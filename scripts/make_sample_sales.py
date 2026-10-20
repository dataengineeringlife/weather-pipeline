"""Makes the sample sales export (dbt/seeds/sales.csv) for every day that has weather data.

Real companies would have a sales CSV from their point-of-sale system. Here we fake one so
the project runs for anyone: rainy days sell more hot drinks, hot days sell more iced coffee.
The numbers are random but repeatable (seeded by city and day).
"""
import csv, json, random
from pathlib import Path

rows = []
for f in sorted(Path("data/raw/weather").glob("date=*/*.json")):
    day, city = f.parent.name.removeprefix("date="), f.stem
    daily = json.loads(f.read_text())["daily"]
    rain = daily["precipitation_sum"][0] or 0
    temp = daily["temperature_2m_max"][0] or 15
    rng = random.Random(f"{city}-{day}")
    hot = round(110 + 3.2 * rain - 1.5 * (temp - 15) + rng.uniform(-8, 8))
    iced = round(60 + 3.0 * max(temp - 15, 0) - 2.3 * rain + rng.uniform(-8, 8))
    rows.append((day, city, max(hot, 0), max(iced, 0)))

out = Path("dbt/seeds/sales.csv")
with out.open("w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["day", "city", "hot_drinks", "iced_drinks"])
    w.writerows(rows)
print(f"wrote {len(rows)} rows to {out}")

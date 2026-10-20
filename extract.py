"""Step 1 + 2: extract daily weather from the free Open-Meteo API and land the raw JSON.

Usage:  python extract.py 2026-10-19
Writes: data/raw/weather/date=2026-10-19/<city>.json  (one file per city, overwritten on re-runs)
"""
import requests, sys
from pathlib import Path

CITIES = {"new_york": (40.71, -74.01), "london": (51.51, -0.13)}

if len(sys.argv) != 2:
    sys.exit("usage: python extract.py YYYY-MM-DD")
day = sys.argv[1]   # e.g. 2026-10-19

for city, (lat, lon) in CITIES.items():
    r = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lat, "longitude": lon,
                "daily": "temperature_2m_max,precipitation_sum",
                "start_date": day, "end_date": day},
        timeout=30)
    r.raise_for_status()
    out = Path(f"data/raw/weather/date={day}/{city}.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(r.text)   # exactly as it arrived
    print(f"saved {out}")

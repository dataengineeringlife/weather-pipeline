"""Run extract.py for each of the last N days (default 14), so the dashboard has history.

Usage:  python scripts/backfill.py        # last 14 days
        python scripts/backfill.py 30     # last 30 days (Open-Meteo's forecast API keeps about 3 months)
"""
import subprocess, sys
from datetime import date, timedelta

days = int(sys.argv[1]) if len(sys.argv) > 1 else 14
for n in range(days, 0, -1):
    day = (date.today() - timedelta(days=n)).isoformat()
    subprocess.run([sys.executable, "extract.py", day], check=True)

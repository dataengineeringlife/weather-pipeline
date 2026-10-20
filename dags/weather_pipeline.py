"""Step 5: the Airflow DAG. Runs extract -> load -> sample sales -> dbt build every day at 06:00.

PROJECT_DIR is the folder that holds extract.py; it defaults to the repo root
(one level above this dags/ folder), and the Docker setup sets it for you.
"""
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator

PROJECT_DIR = os.environ.get("PROJECT_DIR", str(Path(__file__).resolve().parents[1]))

with DAG("weather_pipeline", schedule="0 6 * * *",
         start_date=datetime(2026, 10, 1), catchup=False,
         default_args={"retries": 3, "retry_delay": timedelta(minutes=5)}):
    extract = BashOperator(task_id="extract",
        bash_command="python extract.py {{ ds }}", cwd=PROJECT_DIR)
    load = BashOperator(task_id="load",
        bash_command="python load.py", cwd=PROJECT_DIR)
    # stands in for the sales CSV export a real company would drop here every day
    sample_sales = BashOperator(task_id="sample_sales",
        bash_command="python scripts/make_sample_sales.py", cwd=PROJECT_DIR)
    dbt_build = BashOperator(task_id="dbt_build",
        bash_command="cd dbt && dbt build", cwd=PROJECT_DIR)

    extract >> load >> sample_sales >> dbt_build

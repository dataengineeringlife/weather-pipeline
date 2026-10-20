"""Step 3: load every raw JSON file into the DuckDB warehouse as raw.weather."""
import duckdb

con = duckdb.connect("warehouse.duckdb")
con.sql("create schema if not exists raw")
con.sql("""
  create or replace table raw.weather as
  select * from read_json_auto(
    'data/raw/weather/*/*.json', filename = true)
""")
print(con.sql("select count(*) as files_loaded from raw.weather").fetchone()[0], "files loaded into raw.weather")

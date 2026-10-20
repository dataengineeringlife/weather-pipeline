-- silver: one clean row per city per day
select
  regexp_extract(filename, '(\w+)\.json', 1) as city,
  unnest(daily.time)::date                  as day,
  unnest(daily.temperature_2m_max)          as temp_max_c,
  unnest(daily.precipitation_sum)           as rain_mm
from {{ source('raw', 'weather') }}

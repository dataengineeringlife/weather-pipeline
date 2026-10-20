-- gold: weather joined with sales, one row per city per day
select w.day, w.city, w.temp_max_c, w.rain_mm,
       s.hot_drinks, s.iced_drinks
from {{ ref('stg_weather') }} w
join {{ ref('sales') }} s using (day, city)

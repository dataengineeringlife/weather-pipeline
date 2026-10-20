"""Step 6: the Streamlit dashboard.  Run with:  streamlit run app.py"""
import duckdb, streamlit as st

# open, read, close: DuckDB allows only one writer, so don't hold the file while Airflow loads it
with duckdb.connect("warehouse.duckdb", read_only=True) as con:
    df = con.sql("select * from weather_sales order by day").df()

st.title("Does rain sell more hot coffee?")
city = st.selectbox("Store", df.city.unique())
df = df[df.city == city]
st.line_chart(df, x="day", y=["hot_drinks", "iced_drinks"])
st.bar_chart(df, x="day", y="rain_mm")

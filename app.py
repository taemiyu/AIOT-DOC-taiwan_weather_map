import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import database

st.set_page_config(page_title="Taiwan Weather", page_icon="🌤️", layout="wide")

st.title("🌤️ Taiwan Weather Dashboard")
st.markdown("Sources: `O-A0003-001` (Observations) & `F-D0047-091` (7-Day Forecast)")

try:
    stations = database.query_stations()
    townships = database.query_townships()
    if not stations:
        st.warning("Database is empty. Please run `python setup_data.py` first.")
        st.stop()
except Exception as e:
    st.error(f"Database error: {e}")
    st.warning("Please run `python setup_data.py` first.")
    st.stop()

col1, col2 = st.columns([1, 1])

with col1:
    st.header("🗺️ Current Observation (O-A0003-001)")
    
    selected_station = st.selectbox("Select Station:", stations)
    df_station = database.query_station_observation(selected_station)
    
    if not df_station.empty:
        obs = df_station.iloc[0]
        
        # Display key metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Temperature", f"{obs['temperature']} °C")
        m2.metric("Weather", obs['weather'])
        m3.metric("Observation Time", obs['obsTime'][11:16])
        
    st.subheader("Taiwan Real-time Temperature Map")
    df_all_obs = database.query_all_observations()
    
    if not df_all_obs.empty:
        m = folium.Map(location=[23.7, 121.0], zoom_start=7)
        for _, row in df_all_obs.iterrows():
            if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
                temp = row["temperature"]
                # Color code
                col = "blue" if temp < 20 else "green" if temp < 25 else "orange" if temp < 30 else "red"
                
                folium.CircleMarker(
                    location=[row["lat"], row["lon"]],
                    radius=6,
                    popup=f"<b>{row['stationName']}</b><br>Temp: {temp}°C<br>Wx: {row['weather']}",
                    tooltip=f"{row['stationName']} ({temp}°C)",
                    color=col,
                    fill=True,
                    fillColor=col,
                    fillOpacity=0.7
                ).add_to(m)
        st_folium(m, width=500, height=500, returned_objects=[])

with col2:
    st.header("📍 7-Day Forecast (F-D0047-091)")
    
    selected_township = st.selectbox("Select Township (Forecast):", townships, index=0)
    df_town = database.query_township_forecast(selected_township)
    
    if not df_town.empty:
        st.subheader(f"{selected_township} - Temperature Trend")
        chart_data = df_town.set_index("dataDate")[["mint", "maxt"]]
        st.line_chart(chart_data)
        
        st.subheader("Weekly Detail")
        df_display = df_town.copy()
        if "pop12h" in df_display.columns:
            df_display["pop12h"] = df_display["pop12h"].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) else "-")
            
        st.dataframe(
            df_display.set_index("dataDate"),
            use_container_width=True,
            column_config={
                "mint": "Min °C",
                "maxt": "Max °C",
                "pop12h": "Rain %",
                "wx": "Weather",
            }
        )
    else:
        st.info("No detailed data available for this township.")

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import database
import datetime

# Must be the very first Streamlit command
st.set_page_config(page_title="Taiwan Weather", page_icon="🌤️", layout="wide")

# Custom CSS for the Full-screen Map and Floating Panels
CUSTOM_CSS = """
<style>
/* Remove padding and margin from main blocks */
.block-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
}
/* Hide the top header bar and footer */
header[data-testid="stHeader"] {
    display: none;
}
footer {
    display: none;
}
/* Float Left Panel */
div[data-testid="stVerticalBlock"] > div.stVerticalBlock:nth-child(1) {
    position: absolute;
    top: 20px;
    left: 20px;
    width: 350px;
    z-index: 1000;
    background-color: rgba(22, 27, 34, 0.9);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    color: white;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
/* Float Right Panel */
div[data-testid="stVerticalBlock"] > div.stVerticalBlock:nth-child(2) {
    position: absolute;
    top: 20px;
    right: 20px;
    width: 380px;
    z-index: 1000;
    background-color: rgba(22, 27, 34, 0.9);
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    color: white;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.1);
}
/* Alert Bar (Top Middle) */
.custom-alert {
    position: absolute;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    width: 600px;
    z-index: 1000;
    background-color: rgba(22, 27, 34, 0.9);
    padding: 10px 20px;
    border-radius: 6px;
    border-left: 5px solid #e74c3c;
    color: white;
    font-size: 14px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}
/* Subtitle/Text coloring */
h1, h2, h3, h4, h5, p, label {
    color: #e6edf3 !important;
}
/* Customizing metrics to look like the image */
div[data-testid="stMetricValue"] {
    font-size: 1.8rem !important;
    color: #58a6ff !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Fake top alert element (simulating screenshot)
st.markdown("""
<div class="custom-alert">
    ⚠️ <b>天氣特報</b> 來源：中央氣象署 <br>
    東北風偏強，受鋒面影響，沿海及離島易有強陣風，請注意。
</div>
""", unsafe_allow_html=True)

# Data Initialization
try:
    stations = database.query_stations()
    townships = database.query_townships()
    if not stations:
        st.warning("Database empty.")
        st.stop()
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- Map Background (Rendered first so it falls behind absolute elements) ---
# It's important to render the map BEFORE the column layout in the tree 
# But streamlit renders sequentially. Because our panels are "absolute", they can be anywhere.
# Actually, Streamlit will stack them. Let's create holding boxes.

col1, col2 = st.columns([1, 1])

# Left Panel
with col1:
    st.markdown("### 台灣即時氣象")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    st.markdown(f"<small>更新時間: {now}</small>", unsafe_allow_html=True)
    st.markdown("<small>資料來源: CWA O-A0003-001</small>", unsafe_allow_html=True)
    
    st.divider()

    selected_station = st.selectbox("選擇測站", stations, key="station_select")
    df_station = database.query_station_observation(selected_station)
    
    if not df_station.empty:
        obs = df_station.iloc[0]
        
        m1, m2 = st.columns(2)
        m1.metric("氣溫", f"{obs['temperature']} °C")
        m2.metric("天氣現象", obs['weather'])
        
        # Display extra info
        st.caption(f"觀測站: {obs['countyName']} {obs['stationName']}")
    
    st.divider()
    st.button("↻ 重新整理 (API)", use_container_width=True)

# Right Panel
with col2:
    st.markdown("### 📍 未來一週鄉鎮預報")
    selected_township = st.selectbox("地區選擇", townships, key="township_select")
    df_town = database.query_township_forecast(selected_township)
    
    if not df_town.empty:
        chart_data = df_town.set_index("dataDate")[["mint", "maxt"]]
        # Streamlit line chart defaults to white on dark themes, but line colors can't be deep customized easily
        st.line_chart(chart_data, height=200)
        
        df_display = df_town.copy()
        if "pop12h" in df_display.columns:
             df_display["pop12h"] = df_display["pop12h"].apply(lambda x: f"{x:.0f}%" if pd.notnull(x) else "-")
             
        st.dataframe(
            df_display.set_index("dataDate"),
            use_container_width=True,
            column_config={
                "mint": "最低溫 °C",
                "maxt": "最高溫 °C",
                "pop12h": "雨降率 %",
                "wx": "天氣",
            }
        )
    else:
        st.info("無該地區資料")

# Fullscreen Folium Map
df_all_obs = database.query_all_observations()

m = folium.Map(
    location=[23.7, 121.0], 
    zoom_start=7.5,
    tiles="CartoDB dark_matter" # Best alternative to Esri Dark Gray available out-of-the-box in folium
)

# Plot observations
for _, row in df_all_obs.iterrows():
    if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
        temp = row["temperature"]
        if temp < 15: color = "#1a9850"
        elif temp < 25: color = "#a6d96a"
        elif temp < 30: color = "#fdae61"
        else: color = "#d73027"
        
        # Use simple DivIcon for sleek look
        icon_html = f'''
            <div style="
                background-color: {color};
                border: 2px solid white;
                color: white;
                font-size: 10pt;
                font-weight: bold;
                border-radius: 50%;
                width: 32px;
                height: 32px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 0 5px rgba(0,0,0,0.5);
                ">
                {int(temp)}°
            </div>
        '''
        
        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=f"{row['countyName']} {row['stationName']}<br>{temp}°C {row['weather']}",
            tooltip=row['stationName'],
            icon=folium.DivIcon(html=icon_html, icon_anchor=(16, 16))
        ).add_to(m)

st_folium(
    m, 
    width="100%", 
    height=1200, 
    returned_objects=[]
)

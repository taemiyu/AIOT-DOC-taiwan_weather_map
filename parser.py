import pandas as pd

def parse_observation(data: dict) -> pd.DataFrame:
    """Parse O-A0003-001 current weather observations."""
    records = []
    stations = data.get("records", {}).get("Station", [])
    
    for st in stations:
        try:
            name = st.get("StationName")
            obs_time = st.get("ObsTime", {}).get("DateTime")
            county = st.get("GeoInfo", {}).get("CountyName")
            
            # Coordinates
            lat = lon = None
            for coord in st.get("GeoInfo", {}).get("Coordinates", []):
                if coord.get("CoordinateName") == "WGS84":
                    lat = float(coord["StationLatitude"])
                    lon = float(coord["StationLongitude"])
                    break
            
            we = st.get("WeatherElement", {})
            temp = we.get("AirTemperature")
            weather = we.get("Weather")
            
            if name and obs_time and temp != -99:
                records.append({
                    "stationName": name,
                    "countyName": county,
                    "obsTime": obs_time,
                    "temperature": float(temp),
                    "weather": weather,
                    "lat": lat,
                    "lon": lon
                })
        except Exception as e:
            continue
            
    df = pd.DataFrame(records)
    print(f"[OK] Parsed {len(df)} stations (Observation).")
    return df

def parse_township(data: dict) -> pd.DataFrame:
    """Parse F-D0047-091 7-day forecast."""
    records = []
    
    try:
        # Note capitalization from API
        locations = data["records"]["Locations"][0]["Location"]
    except KeyError:
        return pd.DataFrame()
        
    for doc in locations:
        loc_name = doc.get("LocationName")
        we = {el["ElementName"]: el for el in doc.get("WeatherElement", [])}
        
        mint_el = we.get("最低溫度", {}).get("Time", [])
        maxt_el = we.get("最高溫度", {}).get("Time", [])
        pop_el  = we.get("12小時降雨機率", {}).get("Time", [])
        wx_el   = we.get("天氣現象", {}).get("Time", [])
        
        # Take minimum length to prevent out of bounds
        length = min(len(mint_el), len(maxt_el)) 
        
        for i in range(length):
            try:
                date = mint_el[i]["StartTime"][:10]
                mint = float(mint_el[i]["ElementValue"][0]["MinTemperature"])
                maxt = float(maxt_el[i]["ElementValue"][0]["MaxTemperature"])
                
                # Handling optional fields that might have different lengths or structures
                pop = None
                if i < len(pop_el):
                    p_val = pop_el[i]["ElementValue"][0]["ProbabilityOfPrecipitation"]
                    if p_val and p_val != ' ':
                        pop = float(p_val)
                        
                wx = None
                if i < len(wx_el):
                    wx = wx_el[i]["ElementValue"][0]["Weather"]
                    
                records.append({
                    "locationName": loc_name,
                    "dataDate": date,
                    "mint": mint,
                    "maxt": maxt,
                    "pop12h": pop,
                    "wx": wx
                })
            except Exception:
                continue
                
    df = pd.DataFrame(records)
    # Simplify to just daily data (instead of 12hr precision duplicates for min/max)
    if not df.empty:
        df = df.groupby(["locationName", "dataDate"]).agg({
            "mint": "min",
            "maxt": "max",
            "pop12h": "max", # take max rain probability for the day
            "wx": "first"
        }).reset_index()
    print(f"[OK] Parsed {len(df)} township forecasts.")
    return df

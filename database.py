import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "data.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS StationObservations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            stationName TEXT NOT NULL,
            countyName  TEXT NOT NULL,
            obsTime     TEXT NOT NULL,
            temperature REAL,
            weather     TEXT,
            lat         REAL,
            lon         REAL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS TownshipForecasts (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            locationName TEXT NOT NULL,
            dataDate     TEXT NOT NULL,
            mint         REAL,
            maxt         REAL,
            pop12h       REAL,
            wx           TEXT
        )
    """)
    conn.commit()
    conn.close()
    print("[OK] Database initialized.")

def insert_observation(df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM StationObservations")
    for _, row in df.iterrows():
        cur.execute(
            """INSERT INTO StationObservations 
               (stationName, countyName, obsTime, temperature, weather, lat, lon)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (row["stationName"], row["countyName"], row["obsTime"], 
             row["temperature"], row["weather"], row["lat"], row["lon"])
        )
    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(df)} station observations.")

def insert_township(df: pd.DataFrame):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM TownshipForecasts")
    for _, row in df.iterrows():
        cur.execute(
            """INSERT INTO TownshipForecasts
               (locationName, dataDate, mint, maxt, pop12h, wx)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (row["locationName"], row["dataDate"], row["mint"], row["maxt"], row.get("pop12h"), row.get("wx"))
        )
    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(df)} township forecasts.")

def query_stations() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT stationName FROM StationObservations ORDER BY stationName")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def query_all_observations() -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM StationObservations", conn)
    conn.close()
    return df

def query_station_observation(station: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM StationObservations WHERE stationName=?", conn, params=(station,))
    conn.close()
    return df

def query_townships() -> list:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT locationName FROM TownshipForecasts ORDER BY locationName")
    rows = [r[0] for r in cur.fetchall()]
    conn.close()
    return rows

def query_township_forecast(location: str) -> pd.DataFrame:
    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT dataDate, mint, maxt, pop12h, wx FROM TownshipForecasts WHERE locationName=? ORDER BY dataDate",
        conn, params=(location,)
    )
    conn.close()
    return df

if __name__ == "__main__":
    init_db()

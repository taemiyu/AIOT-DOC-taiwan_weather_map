---
description: Taiwan Weather Forecast — Full Project Development Workflow
---

# 🌤️ Taiwan Weather Forecast — Project Workflow

## ✅ Phase 1: Environment Setup

1. Create and activate a Python virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

// turbo
2. Install all required dependencies
```bash
pip install requests pandas streamlit folium streamlit-folium
```

// turbo
3. Confirm installations
```bash
pip list | findstr /i "requests pandas streamlit folium"
```

---

## ✅ Phase 2: CWA API Setup

4. Register at [CWA Open Data Platform](https://opendata.cwa.gov.tw/) and obtain your API Key

5. Create a `.env` file (or `config.py`) to store your API Key securely
```
CWA_API_KEY=your_api_key_here
```

6. Test API connection — fetch weather JSON data
```bash
python fetch_weather.py
```

---

## ✅ Phase 3: Data Processing

7. Parse the JSON response and extract `MinT` / `MaxT` for each region
```bash
python parse_weather.py
```

// turbo
8. Use Pandas to clean and structure the data into a DataFrame
```bash
python preprocess.py
```

---

## ✅ Phase 4: SQLite Database

// turbo
9. Initialize the SQLite database and create the `TemperatureForecasts` table
```bash
python init_db.py
```

10. Insert processed weather data into the database
```bash
python insert_data.py
```

// turbo
11. Verify data with SQL query
```bash
python verify_db.py
```

---

## ✅ Phase 5: Streamlit Web App

12. Build the Streamlit app (`app.py`) with the following features:
    - 🔽 Dropdown to select region (北部、中部、南部、東部、東南部)
    - 📈 Line chart: MaxT vs MinT for the week
    - 📋 Data table: date-by-date temperature breakdown
    - 🗺️ (Advanced) Taiwan map with color-coded temperature

// turbo
13. Run the Streamlit app locally
```bash
streamlit run app.py
```

14. Open browser at `http://localhost:8501` and verify the dashboard

---

## ✅ Phase 6: Map Visualization (Advanced)

15. Install Folium integration
```bash
pip install folium streamlit-folium
```

16. Add map component to `app.py`:
    - Select date from dropdown
    - Display Taiwan regions color-coded by average temperature
    - Color scale: Blue (<20°C) → Green (20-25°C) → Yellow (25-30°C) → Red (>30°C)

// turbo
17. Re-run the app to verify map rendering
```bash
streamlit run app.py
```

---

## ✅ Phase 7: Code Quality

18. Review and improve:
    - [ ] Clear code structure and comments
    - [ ] Error handling (try/except for API & DB)
    - [ ] No duplicate code (DRY principle)
    - [ ] Meaningful variable names

---

## ✅ Phase 8: GitHub Deployment

// turbo
19. Stage all project files
```bash
git add .
```

20. Commit with a descriptive message
```bash
git commit -m "feat: Taiwan Weather Forecast Web App - initial release"
```

21. Push to GitHub
```bash
git push -u origin main
```

22. Verify at `https://github.com/taemiyu/AIOT-DOC-taiwan_weather_map`

---

## 💡 Extension Ideas (Phase 9+)

- [ ] Line Bot weather alert notifications
- [ ] Travel itinerary recommendation engine
- [ ] Agricultural / disaster prevention alerts
- [ ] AI-powered weather trend analysis

---

## 📁 Recommended Project Structure

```
AIOT-L3-CWA/
├── app.py                  # Main Streamlit app
├── fetch_weather.py        # CWA API data fetching
├── parse_weather.py        # JSON parsing & extraction
├── preprocess.py           # Pandas data cleaning
├── init_db.py              # SQLite DB initialization
├── insert_data.py          # Insert data into DB
├── verify_db.py            # SQL query verification
├── data.db                 # SQLite database file
├── config.py               # API key & settings
├── requirements.txt        # Dependencies
├── README.md               # Project documentation
└── .agents/
    └── workflows/
        └── taiwan_weather_workflow.md
```

---

> *"AI × Data × Real World — 用技術創造更好的未來！"*

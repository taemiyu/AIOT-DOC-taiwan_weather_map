# Taiwan Weather Forecast --- Development Workflow

## 1. Project Overview

This project builds a Taiwan weather forecast application using:

-   CWA Open Data API
-   Python
-   Requests
-   JSON parsing
-   Pandas
-   SQLite3
-   SQL
-   Streamlit
-   Folium / Leaflet for map visualization
-   GitHub
-   Streamlit Community Cloud

The implementation should first satisfy the HW10 requirements and then
add visualization and deployment enhancements.

------------------------------------------------------------------------

## 2. Core Requirements

The project must support the following workflow:

``` text
CWA API
   ↓
JSON
   ↓
JSON Parsing
   ↓
Extract MinT / MaxT
   ↓
Pandas DataFrame
   ↓
SQLite3
   ↓
SQL Query
   ↓
Streamlit
   ↓
Dropdown + Line Chart + Table
```

### Required regions

The forecast data must cover:

-   北部地區
-   中部地區
-   南部地區
-   東北部地區
-   東部地區
-   東南部地區

### Required database

Database:

``` text
data.db
```

Table:

``` text
TemperatureForecasts
```

Required columns:

``` text
id
regionName
dataDate
mint
maxt
```

------------------------------------------------------------------------

## 3. Development Principle

Use Antigravity as the primary coding agent.

ChatGPT is used as the technical planning and review assistant.

### Responsibilities

**Antigravity**

-   Create and modify project files
-   Run Python code
-   Install dependencies
-   Run tests
-   Debug implementation problems
-   Run Streamlit locally
-   Perform Git operations when requested

**ChatGPT**

-   Design the architecture
-   Break the project into implementation phases
-   Write precise prompts for Antigravity
-   Explain Python / JSON / SQL / SQLite / Streamlit concepts
-   Review generated code
-   Diagnose errors
-   Check implementation against the assignment requirements
-   Review GitHub and deployment readiness

Do not ask Antigravity to implement the entire project in one step.

Each phase must be completed and verified before moving to the next
phase.

------------------------------------------------------------------------

# 4. Project Structure

The target project structure is:

``` text
taiwan-weather-forecast/
│
├── app.py
├── cwa_api.py
├── parser.py
├── database.py
├── requirements.txt
├── README.md
├── workflow.md
├── .gitignore
│
├── data/
│   └── .gitkeep
│
└── tests/
    ├── test_parser.py
    └── test_database.py
```

The database file should not be committed to GitHub.

Recommended ignored files:

``` text
.venv/
__pycache__/
*.pyc
.env
*.db
*.sqlite
*.sqlite3
.DS_Store
```

------------------------------------------------------------------------

# 5. Phase 0 --- Environment Setup

## Goal

Create a clean Python development environment.

### Tasks

1.  Create the project directory.
2.  Create `.venv`.
3.  Install required packages.
4.  Create `.gitignore`.
5.  Create `requirements.txt`.
6.  Create the initial README.
7.  Verify Python and package versions.

### Required packages

``` text
requests
pandas
streamlit
folium
streamlit-folium
```

SQLite3 is provided by Python and normally does not need to be installed
through pip.

### Verification

Run:

``` bash
python --version
```

and:

``` bash
pip list
```

Do not proceed until the environment works.

------------------------------------------------------------------------

# 6. Phase 1 --- GitHub Repository

## Goal

Put the project under Git version control from the beginning.

### Repository

Recommended name:

``` text
taiwan-weather-forecast
```

### Initial Git workflow

``` bash
git init
git add .
git commit -m "Initial project setup"
git branch -M main
git remote add origin <GITHUB_REPOSITORY_URL>
git push -u origin main
```

### Important

Never commit:

-   CWA API keys
-   `.env`
-   passwords
-   tokens
-   local database files
-   private credentials

------------------------------------------------------------------------

# 7. Phase 2 --- CWA API

## Goal

Fetch the required one-week forecast data from CWA.

Dataset:

``` text
F-A0010-001
```

The implementation must use the JSON API.

### Module

``` text
cwa_api.py
```

### Responsibilities

`cwa_api.py` should:

1.  Read the CWA API key securely.
2.  Build the API request.
3.  Send the request using `requests`.
4.  Check the HTTP response.
5.  Convert the response to JSON.
6.  Return the JSON object to the parser.
7.  Handle request errors clearly.

### API key rule

Never hard-code the real API key.

Local development may use:

``` text
.env
```

Streamlit deployment should use Streamlit Secrets.

Example application access:

``` python
import streamlit as st

api_key = st.secrets["CWA_API_KEY"]
```

The exact secret-loading implementation may be adapted for local
development.

### JSON inspection

The first successful API request must be inspected with:

``` python
json.dumps(data, ensure_ascii=False, indent=2)
```

Do not guess the JSON structure.

------------------------------------------------------------------------

# 8. Phase 3 --- JSON Analysis and Parsing

## Goal

Understand the actual CWA JSON structure and extract the required data.

### Module

``` text
parser.py
```

### Required output

The parser must produce records containing:

``` text
regionName
dataDate
mint
maxt
```

### Expected logical structure

``` text
CWA JSON
   ↓
locations
   ↓
location
   ↓
weatherElements
   ↓
MinT / MaxT
   ↓
daily records
```

The exact field path must be verified from the actual API response
before implementation.

### Required regions

``` text
北部地區
中部地區
南部地區
東北部地區
東部地區
東南部地區
```

### Validation

After parsing, verify:

-   All required regions exist.
-   Dates are valid.
-   MinT values are numeric.
-   MaxT values are numeric.
-   No accidental duplicate records exist.
-   The number of days is consistent with the requested forecast period.

------------------------------------------------------------------------

# 9. Phase 4 --- Pandas DataFrame

## Goal

Convert parsed records into a clean DataFrame.

Expected columns:

``` text
regionName
dataDate
mint
maxt
```

Example:

``` text
regionName  dataDate    mint  maxt
北部地區      2026-09-16  24    31
北部地區      2026-09-17  25    32
中部地區      2026-09-16  25    32
```

### Validation

Use:

``` python
df.head()
df.info()
df.describe()
```

Check for:

``` python
df.isna().sum()
```

and duplicates:

``` python
df.duplicated().sum()
```

------------------------------------------------------------------------

# 10. Phase 5 --- CSV Export

## Goal

Save the parsed forecast data as:

``` text
weather_data.csv
```

Recommended:

``` python
df.to_csv(
    "weather_data.csv",
    index=False,
    encoding="utf-8-sig"
)
```

CSV is an intermediate/export format.

The required application database remains SQLite.

------------------------------------------------------------------------

# 11. Phase 6 --- SQLite Database

## Goal

Create:

``` text
data.db
```

with:

``` text
TemperatureForecasts
```

### Schema

``` sql
CREATE TABLE TemperatureForecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regionName TEXT NOT NULL,
    dataDate TEXT NOT NULL,
    mint REAL,
    maxt REAL
);
```

### Module

``` text
database.py
```

### Responsibilities

-   Create database
-   Create table
-   Insert forecast records
-   Query region names
-   Query regional forecast data
-   Query date-specific data
-   Close database connections safely

------------------------------------------------------------------------

# 12. Phase 7 --- Database Validation

The application must verify that the data was correctly inserted.

### Query all regions

``` sql
SELECT DISTINCT regionName
FROM TemperatureForecasts;
```

### Query Central Taiwan

``` sql
SELECT *
FROM TemperatureForecasts
WHERE regionName = '中部地區'
ORDER BY dataDate;
```

### Query one region

``` sql
SELECT *
FROM TemperatureForecasts
WHERE regionName = ?
ORDER BY dataDate;
```

Do not hard-code SQL values when parameters can be used.

------------------------------------------------------------------------

# 13. Phase 8 --- Streamlit MVP

## Goal

Build the required Streamlit application.

### Main file

``` text
app.py
```

### Required UI

The application must provide:

1.  Region dropdown
2.  SQLite-based SQL query
3.  One-week temperature data
4.  Line chart
5.  Data table

Logical flow:

``` text
User selects region
       ↓
Streamlit
       ↓
SQL query
       ↓
SQLite
       ↓
DataFrame
       ↓
Chart + Table
```

The Streamlit application must not bypass SQLite by reading the CSV
directly for the required database query functionality.

------------------------------------------------------------------------

# 14. Phase 9 --- Streamlit Layout

Target layout:

``` text
┌─────────────────────────────────────────────┐
│       Taiwan Weather Forecast               │
├──────────────────────┬──────────────────────┤
│                      │                      │
│ Region selector      │ Temperature table    │
│                      │                      │
│ Taiwan map            │                      │
│                      │ Line chart            │
│                      │                      │
└──────────────────────┴──────────────────────┘
```

Use Streamlit columns for the left-right layout.

------------------------------------------------------------------------

# 15. Phase 10 --- Folium Taiwan Map

This is an enhancement after the required HW10 functionality works.

## Goal

Add an interactive Taiwan map.

Use:

``` text
folium
streamlit-folium
```

### Initial region coordinates

Use approximate coordinates for the six forecast regions.

The coordinates are visualization points, not official administrative
boundaries.

### Marker logic

Calculate:

``` python
avg_temp = (mint + maxt) / 2
```

Then classify:

``` text
< 20°C       blue
20–25°C      green
25–30°C      yellow
> 30°C       red
```

### Popup

Each marker should display:

``` text
Region
Date
Min Temperature
Max Temperature
Average Temperature
```

------------------------------------------------------------------------

# 16. Phase 11 --- Date Selection

Add a date selector.

Logical flow:

``` text
Select Date
     ↓
SQL query / filtered dataset
     ↓
Six regions
     ↓
Map markers
     ↓
Temperature colors
     ↓
Table
```

The selected date must update the displayed data dynamically.

------------------------------------------------------------------------

# 17. Phase 12 --- GitHub Auto Deploy

The production workflow is:

``` text
Local development
       ↓
Antigravity
       ↓
Run tests
       ↓
Git commit
       ↓
Git push
       ↓
GitHub
       ↓
Streamlit Community Cloud
       ↓
Automatic deployment
```

After the initial Streamlit deployment, future changes should normally
follow:

``` bash
git add .
git commit -m "Describe the change"
git push
```

Streamlit Community Cloud should then rebuild/redeploy the application
from the configured GitHub repository.

------------------------------------------------------------------------

# 18. Phase 13 --- Streamlit Secrets

Do not commit the CWA API key.

Configure the production secret in Streamlit:

``` toml
CWA_API_KEY = "YOUR_CWA_API_KEY"
```

Application code should retrieve it through Streamlit Secrets.

Never put the real value in:

-   Python source
-   README
-   GitHub repository
-   screenshots
-   commit messages
-   public documentation

------------------------------------------------------------------------

# 19. Phase 14 --- Deployment Validation

After deployment, verify:

### API

-   CWA API request succeeds.
-   API key is loaded from secrets.
-   Errors are handled.

### Data

-   Six regions appear.
-   Forecast dates appear.
-   MinT and MaxT are numeric.

### SQLite

-   `data.db` can be created.
-   `TemperatureForecasts` exists.
-   SQL queries work.

### Streamlit

-   App starts.
-   Dropdown works.
-   Date selector works.
-   Line chart renders.
-   Table renders.
-   Map renders.
-   Marker popups work.

### Deployment

-   GitHub repository is connected.
-   Streamlit app is accessible.
-   A new GitHub commit triggers a new deployment.

------------------------------------------------------------------------

# 20. Error Handling

Every major stage should have clear error handling.

### CWA API

Handle:

-   connection failure
-   timeout
-   HTTP errors
-   invalid JSON
-   missing API key

### JSON parser

Handle:

-   missing fields
-   unexpected structure
-   missing temperature values
-   invalid numeric values

### SQLite

Handle:

-   database connection failure
-   table creation failure
-   insertion failure
-   SQL query errors

### Streamlit

Display user-friendly errors instead of raw tracebacks when possible.

------------------------------------------------------------------------

# 21. Testing Strategy

Do not wait until the end to test everything.

Test after each phase.

``` text
Phase 0
  ↓
Environment test

Phase 1
  ↓
Git test

Phase 2
  ↓
API test

Phase 3
  ↓
Parser test

Phase 4
  ↓
DataFrame test

Phase 5
  ↓
CSV test

Phase 6
  ↓
SQLite test

Phase 7
  ↓
SQL test

Phase 8
  ↓
Streamlit test

Phase 10
  ↓
Map test

Phase 12
  ↓
Deployment test
```

------------------------------------------------------------------------

# 22. Antigravity Workflow

For every implementation phase, use this pattern:

``` text
1. Give Antigravity one clearly defined task.
2. Ask it to inspect the existing project first.
3. Ask it to make the smallest necessary changes.
4. Ask it to run the relevant tests.
5. Inspect the result.
6. Fix errors before moving forward.
7. Commit the completed phase.
8. Push to GitHub when appropriate.
9. Continue to the next phase.
```

Do not allow an agent to silently rewrite unrelated files.

------------------------------------------------------------------------

# 23. Prompt Style for Antigravity

Each prompt should contain:

``` text
Goal
Context
Requirements
Constraints
Files to modify
Validation steps
Expected result
```

Example:

``` text
Goal:
Implement the CWA API client.

Context:
The project currently contains cwa_api.py but no API implementation.

Requirements:
- Use requests.
- Use F-A0010-001.
- Load the API key securely.
- Return parsed JSON.
- Add timeout handling.
- Do not hard-code the API key.

Validation:
- Run the script.
- Verify HTTP status.
- Print a small JSON preview.
- Do not print the API key.

Do not modify Streamlit or SQLite code yet.
```

------------------------------------------------------------------------

# 24. Git Commit Strategy

Use small, meaningful commits.

Recommended examples:

``` text
Initial project setup
Add CWA API client
Add JSON weather parser
Add weather CSV export
Add SQLite database
Add SQL validation queries
Add Streamlit forecast viewer
Add Folium Taiwan map
Add date filtering
Prepare Streamlit deployment
Improve error handling
```

Avoid:

``` text
update
fix
test
aaa
final
final2
final_final
```

------------------------------------------------------------------------

# 25. Definition of Done

## HW10 MVP

The project is considered complete when:

-   CWA API data is successfully retrieved.
-   JSON structure is inspected.
-   MinT and MaxT are correctly extracted.
-   Six required regions are handled.
-   Forecast data is stored in SQLite.
-   `TemperatureForecasts` contains the required columns.
-   Region names can be queried.
-   中部地區 data can be queried.
-   Streamlit uses SQL to retrieve data.
-   Region dropdown works.
-   Line chart works.
-   Data table works.

## Extended Version

After MVP:

-   Folium Taiwan map
-   Temperature color markers
-   Date selector
-   Popups
-   Left-right dashboard layout

## Deployment Version

Finally:

``` text
GitHub
   ↓
Streamlit Community Cloud
   ↓
Auto Deploy
```

The application must run successfully from the deployed environment
without exposing secrets.

------------------------------------------------------------------------

# 26. Future Advanced Version

Do not implement these until the MVP is stable.

Possible future architecture:

``` text
CWA Open Data
      ↓
FastAPI
      ↓
Normalize
      ↓
Validate
      ↓
Cache / Database
      ↓
REST API
      ↓
React / Next.js
      ↓
Leaflet
      ↓
Windy Map
      ↓
CWA Temperature Overlay
```

Potential future features:

-   CWA observation data
-   Station-level temperature
-   Humidity
-   Pressure
-   Wind speed
-   Wind direction
-   Precipitation
-   Automatic refresh
-   County filter
-   Station search
-   Heatmap
-   Historical playback
-   Forecast vs. actual temperature comparison
-   Machine learning analysis

These are extensions and must not replace the required HW10
implementation.

------------------------------------------------------------------------

# 27. Final Development Principle

Build in this order:

``` text
Correctness
    ↓
Testability
    ↓
Database
    ↓
Streamlit MVP
    ↓
Visualization
    ↓
GitHub
    ↓
Auto Deployment
    ↓
Advanced Architecture
```

Do not optimize the UI before the data pipeline is correct.

The most important pipeline is:

``` text
CWA API
 → JSON
 → Parser
 → DataFrame
 → SQLite
 → SQL
 → Streamlit
```

Once this pipeline is stable, add the Taiwan map and advanced features.

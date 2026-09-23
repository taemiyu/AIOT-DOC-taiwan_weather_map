import requests
import os
import urllib3
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()
CWA_API_KEY = os.getenv("CWA_API_KEY")
BASE_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore"

def fetch_observation():
    """Fetch O-A0003-001 current weather observations."""
    if not CWA_API_KEY:
        raise ValueError("CWA_API_KEY not found.")
    url = f"{BASE_URL}/O-A0003-001"
    params = {"Authorization": CWA_API_KEY, "format": "JSON"}
    response = requests.get(url, params=params, timeout=30, verify=False)
    response.raise_for_status()
    print("[OK] Fetched O-A0003-001 (Observations).")
    return response.json()

def fetch_township_forecast():
    """Fetch F-D0047-091 township 7-day forecast."""
    if not CWA_API_KEY:
        raise ValueError("CWA_API_KEY not found.")
    url = f"{BASE_URL}/F-D0047-091"
    params = {"Authorization": CWA_API_KEY, "format": "JSON"}
    response = requests.get(url, params=params, timeout=30, verify=False)
    response.raise_for_status()
    print("[OK] Fetched F-D0047-091 (Townships).")
    return response.json()

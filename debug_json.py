import cwa_api
import json

town_json = cwa_api.fetch_township_forecast()
locations = town_json["records"]["Locations"][0]["Location"]
loc = locations[0]
for el in loc["WeatherElement"]:
    if el["ElementName"] == "最高溫度":
        print("MaxT found! Sample:")
        print(json.dumps(el["Time"][:1], ensure_ascii=False, indent=2))
        
        # Test the loop as done in parser.py
        try:
            val = float(el["Time"][0]["ElementValue"][0]["Temperature"])
            print(f"Temperature is: {val}")
        except Exception as e:
            print("Error parsing temperature:", e)
            print("ElementValue is:", el["Time"][0].get("ElementValue"))

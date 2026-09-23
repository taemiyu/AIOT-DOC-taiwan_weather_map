import cwa_api
import parser
import database

def main():
    print("Initializing Database...")
    database.init_db()

    print("\nFetching Observation Data (O-A0003-001)...")
    try:
        obs_json = cwa_api.fetch_observation()
        df_obs = parser.parse_observation(obs_json)
        database.insert_observation(df_obs)
    except Exception as e:
        print(f"Failed to fetch/parse observation data: {e}")

    print("\nFetching Township Data (F-D0047-091)...")
    try:
        town_json = cwa_api.fetch_township_forecast()
        df_town = parser.parse_township(town_json)
        database.insert_township(df_town)
    except Exception as e:
        print(f"Failed to fetch/parse township data: {e}")

    print("\n[DONE] Data setup complete!")

if __name__ == "__main__":
    main()

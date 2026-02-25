import urequests

class SeaLevelPressure:
    def __init__(self): 
        self.locations = {
            "Tettnang": {"lat": 47.66857, "lon": 9.59132},
            "Meckenbeuren": {"lat": 47.70063, "lon": 9.56267},
            "Kressbronn": {"lat": 47.59516, "lon": 9.59727}
        }
        # fallback pressure, if API fails
        self.fallback_pressure = 1013.25 

    def fetch_current(self, city_name):
        print(f"Fetching live sea-level pressure for {city_name}")
        
        # look up the coordinates in dictionary
        coords = self.locations.get(city_name)
            
        # dynamically build the URL for this specific request
        lat = coords["lat"]
        lon = coords["lon"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=pressure_msl"
        
        try:
            # send request to Open-Meteo
            response = urequests.get(url)
            weather_data = response.json()
            
            # extract the exact value
            live_pressure = weather_data['current']['pressure_msl']
            response.close() # close to save RAM
            
            print(f"API Success ({city_name}): {live_pressure} hPa")
            return float(live_pressure)
            
        except Exception as e:
            print(f"API Fetch Failed ({e}). Using fallback: {self.fallback_pressure} hPa")
            return self.fallback_pressure

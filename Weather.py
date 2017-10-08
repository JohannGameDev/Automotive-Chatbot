import requests
import json

class Weather(object):
    def __init__(self):
        self.weather_address = "http://127.0.0.1:8000/api/weather/"


    def get_weather(self,location):
        #TODO:ADD CASE IF NO WEATHER INFO WAS GIVIN BACK
        r = requests.get(self.weather_address+location)
        weather_data = r.json()
        if weather_data.get("temperature",None)!= None:
            temperature = str(weather_data.get("temperature").get("current"))
        else:
            temperature = "temperature_unknown"

        if weather_data.get("weather",None)!= None:
            weather_description = weather_data.get("weather").get("description")
        else:
            weather_description = "Weather unknown"
        return temperature,weather_description

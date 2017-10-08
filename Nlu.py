import requests
import json
from context import Context

class Nlu(object):

    def __init__(self,context):
        self.rasa_adress = "http://localhost:5000/parse?q="
        self.entityNames = {"location_city", "location_street", "location_dest_nl"
                            , "location_current_nl", "time", "calendar_event", "time"}
        self.context = context

    def get_Data(self,message):
        r = requests.get(self.rasa_adress+message)
        print(r.json())
        data = r.json()[0]
        return data

    def parse_massage(self,message):
        raw_data = self.get_Data(message)
        intent = raw_data.get("intent",None)
        entities = self.extract_entities(raw_data)
        confidence = raw_data.get("confidence",None)
        return intent,entities,confidence

    def get_intent(self,message):
        raw_data = self.get_Data(message)
        intent = raw_data.get("intent",None)
        return intent

    def get_entities(self,message):
        raw_data = self.get_Data(message)
        entities = self.extract_entities(raw_data)
        return entities

    def get_full_Location(self,entities):
        destination_location = ""
        current_location = self.context.current_location
        if "location_street" in entities or "location_city" in entities:
            if "location_street" in entities and "location_city" in entities:
                destination_location = entities["location_city"] + " " + entities["location_street"]
            elif "location_city" in entities:
                destination_location = entities["location_city"]
            elif "location_street" in entities:
                destination_location = entities["location_street"]
            self.context.set_current_destination(destination_location)
            self.context.update_queried_location(destination_location)
        if "location_dest_nl" in entities:
            destination_location = self.context.current_destination
            self.context.update_queried_location(destination_location)
        if "location_current_nl" in entities:
            current_location = self.context.current_location
            self.context.update_queried_location(current_location)

        print destination_location
        return current_location,destination_location

    def extract_entities(self,rasa_json):
        entities = {}
        if rasa_json.get("entities",None) != None:
            entitiesJson = rasa_json.get("entities")
            for entityName in self.entityNames:
                if entitiesJson.get(entityName,None) != None:
                    entities[entityName] = entitiesJson.get(entityName).get("value")
        return entities

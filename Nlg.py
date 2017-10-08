# -*- coding: utf-8 -*-


import random


class Nlg(object):

    def __init__(self):
        self.dauer_route = [u"Die Dauer der Route nach {location_string} beträgt {traveling_time_string} ",
                            u"Es dauert {traveling_time_string} um nach {location_string} zu kommen"]
        self.event = [u"Der Event: {event_summary} startet zu dem Zeitpunkt: {event_start}. Das Event befindet sich in der {location}. Deine Notizen für das Event sind:{description}."]
        self.temperatur = [u"In {location} ist es gerade {temperatur}°C und der Wetterzustand ist "
                           u"{weather_description}.",
                           u"Die aktuelle Temperatur ist {temperatur}°C. In {location} und die Wetterlage ist"
                           u" {weather_description}."]

        self.fuel_distance = [u"Dein Tankstand beträgt {fuel_percentage} %."
                              u" Damit kannst du noch {range_distance} km fahren.", u"Mit deinem akutellen Tank {fuel_percentage} %, schaffst du noch {range_distance} km."]
        self.no_event = [u"Kein Event gefunden"]
        self.windows_general = [u"Das vordere linke Fenster ist {front_left}. Das vordere rechte Fenster ist "
                                u"{front_right}. Das hintere linke Fenster ist {rear_left}."
                                u" Das hintere rechte Fenster ist {rear_right}"]
        self.position = [u"Dein Auto steht {address_line}."]
        self.greet = [u"Hallo!",u"Guten Tag",u"Howdy",u"Grüße dich"]
        self.distance = [u"Die Dauer der Route nach {location} dauert {traveling_time}. Die Entfernung beträgt "
                         u"{distance} km."]
        self.doors = [u" Deine vordere linke Tür hat den Schließ-Status : {front_left_closed} und den "
                      u"Verriegelungs-Status: {front_left_locked}. Deine vordere rechte Tür hat den Schließ-Status :"
                      u" {front_right_closed} und den Verriegelungs-Status: {front_right_locked}."
                      u" Deine hintere rechte Tür hat den Schließ-Status : {rear_right_closed} und den"
                      u" Verriegelungs-Status: {rear_right_locked}. Deine hintere linke Tür hat den Schließ-Status :"
                      u" {rear_left_closed} und den Verriegelungs-Status: {rear_left_locked}."]
        self.destination_question = [u"Wohin möchtest du denn?", u"Welches Ziel soll ich ansteuern?",
                                     u"Hast du ein Zielort parat?"]
        self.user_request = [u"Wer will den mit?", u"Wer soll den mitkommen?"]
        self.user_location = [u"Wo wohnst du?",u"Wo bist du?"]

    def human_readable_time(self,seconds):
        human_readable_string = ""
        if seconds / 3600 > 1:
            minutes = str(((seconds % 3600) / 60))
            hours = str(seconds / 3600)
            human_readable_string = hours + " Stunden und " + minutes + " Minuten"
        else:
            human_readable_string = str(seconds/60) +" Minuten"

        return human_readable_string

    def parse_time(self,time):
        if ":" in time:
            timeHour = int(time.split(":")[0])#17
            timeMinute = int(time.split(":")[1])#00
        else:
            timeHour = int(time)#17
            timeMinute = 0
        return timeHour,timeMinute

    def human_distance(self,distance):
        return int(round(distance))

    def create_message(self,message_type=None,message="Something unexpected happend.",text_data=None):

        if message_type == None:
            return message
        if message_type == "dauer_route":
            message = random.choice(self.dauer_route).format(location_string=text_data["destination_location"],traveling_time_string=self.human_readable_time(text_data["traveling_time"]))
        if message_type == "event":
            message = random.choice(self.event).format(event_start=text_data["start_time"],location=text_data["location"],description=text_data["description"],event_summary=text_data["summary"])
        if message_type == "no_event":
            message = random.choice(self.no_event)
        if message_type == "weather":
            message = random.choice(self.temperatur).format(location=text_data["location"],temperatur=text_data["temperature"],weather_description=text_data["weather_description"])
        if message_type == "fuel_distance":
            message = random.choice(self.fuel_distance).format(fuel_percentage=text_data["fuel_percentage"],
                                                               fuel_state=text_data["fuel_state"],
                                                               range_state=text_data["range_state"],
                                                               range_distance=text_data["range_distance"])
        if message_type == "windows_question":
            message = random.choice(self.windows_general).format(front_left=text_data["front_left"],front_right=text_data["front_right"],rear_left=text_data["rear_left"],rear_right=text_data["rear_right"])
        if message_type == "car_position":
            message = random.choice(self.position).format(address_line=text_data["address_line"])
        if message_type == "greet":
            message = random.choice(self.greet)
        if message_type == "distance":
            message = random.choice(self.distance).format(location=text_data["location"],distance=self.human_distance(text_data["distance"]),traveling_time=self.human_readable_time(text_data["duration_seconds"]))
        if message_type == "doors":
            message = random.choice(self.doors).format(front_left_closed=text_data["frontLeft"]["closed_state"],
                                                       front_left_locked=text_data["frontLeft"]["locked_state"],
                                                       front_right_closed=text_data["frontRight"]["closed_state"],
                                                       front_right_locked=text_data["frontRight"]["locked_state"],
                                                       rear_right_closed=text_data["rearRight"]["closed_state"],
                                                       rear_right_locked=text_data["rearRight"]["locked_state"],
                                                       rear_left_closed=text_data["rearLeft"]["closed_state"],
                                                       rear_left_locked=text_data["rearLeft"]["locked_state"])

        if message_type == "destination_question":
            message = random.choice(self.destination_question)
        if message_type == "user_request":
            message = random.choice(self.user_request)
        if message_type == "user_location":
            message = random.choice(self.user_location)

        return message

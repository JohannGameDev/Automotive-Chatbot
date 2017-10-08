from Car import Car
from Calendar import Calendar
from Weather import Weather
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from dateutil import parser
from automotive_bot_statemachine import AutomotiveBotStateMachine
from user import User

class Actions(object):
    def __init__(self, chatbot_delegator):
        self.route_id = 0
        self.home_location = "Carnotstr.4"
        self.reminder_length = 5  # in minutes
        self.chatbot_delegator = chatbot_delegator
        self.car = Car()
        self.savedRoutes = {}
        self.calendar = Calendar()
        self.scheduler = BackgroundScheduler()
        self.schedule_events()
        self.weather = Weather()
        self.state_machine = AutomotiveBotStateMachine()
        self.current_route = {}
        self.current_group_route = {"event_route": False, "current": "", "location": "", "event_name": "", "dest": []}
        self.user = User()

        try:
            self.chatbot_delegator.context.current_location = self.car.get_position()["address_line"] # Rest Api doesnt work
        except:
            print "Cannot find GPS. Set current location to carnotstr.4"
            self.chatbot_delegator.context.current_location = "Carnotstr.4"

    # Schedule route_request to user from event in google calendar
    def schedule_events(self):
        # http://apscheduler.readthedocs.io/en/3.3.1/userguide.html?highlight=missed#missed-job-executions-and-coalescing
        self.scheduler.print_jobs()
        events = self.calendar.get_events()
        for event in events:
            start_time = parser.parse(event['start'].get('dateTime', event['start'].get('date')))
            reminder_time = start_time - datetime.timedelta(minutes=self.reminder_length)
            self.scheduler.add_job(self.handle_event, "date", run_date=reminder_time,
                                   args=[event])
        self.scheduler.start()

    # If a scheduled event is upcoming, handle it
    def handle_event(self, event):
        start = event['start'].get('dateTime', event['start'].get('date'))
        des = event.get("description", None)
        text_data = {"start_time": start, "location": event['location'], "summary": event['summary'], "description": des}
        self.chatbot_delegator.sendMessage(message_type="event", text_data=text_data)
        self.plan_route(event["location"])
        print event["summary"]

    def predict_action(self, intent, entities, confidence, chat_message_info=""):
        if self.state_machine.state == "intent_handling":
            self.select_action(intent, entities, confidence, chat_message_info)

        elif self.state_machine.state == "plan_route":
            _, current_destination = self.chatbot_delegator.nlu.get_full_Location(entities)
            self.plan_route(chat_message_info, current_location=self.current_route["current_location"],
                                     current_destination=current_destination, time = self.current_route["time"])
            self.state_machine.route_finished()
        elif self.state_machine.state == "plan_group_route":
            if intent == "accompany_intent":
                if self.user.is_existing_user(chat_message_info.user_message_id):
                    self.current_group_route["dest"].append(self.user.get_user_address(chat_message_info.user_message_id))
                else:
                    self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="user_location")
                    self.state_machine.ask_user()
            if intent == "plan_intent":
                self.plan_group_route(chat_message_info)
                self.state_machine.group_route_planned()

        elif self.state_machine.state == "ask_user_address":
            _, location = self.chatbot_delegator.nlu.get_full_Location(entities)
            self.current_group_route["dest"].append(location)
            self.user.add_user(chat_message_info.user_message_id,chat_message_info.user_name,location)
            self.state_machine.got_address()







        else:
            print "Some Undefinded State"




    # for given intent and entities pick the right action
    def select_action(self, intent, entities, confidence, chat_message_info=""):
        self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="send_action", text_data={"action_type": "typing"})
        print "The Chat id is from predict_action: " + str(chat_message_info)
        current_location, current_destination = self.chatbot_delegator.nlu.get_full_Location(entities)
        if intent == "route_intent" and  not chat_message_info.is_group_chat_message:
            if "calendar_event" in entities:  # handle if no event_type is found.
                calendar_event = entities["calendar_event"]
                self.plan_event_route(chat_message_info, current_location, calendar_event)
            elif not current_destination:
                                self.current_route["current_location"] = current_location
                                self.current_route["time"] = entities.get("time", None)
                                self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="destination_question")
                                self.state_machine.plan_route()
            else:
                self.plan_route(chat_message_info, current_location, current_destination, time=entities.get("time", None))

        if intent == "route_intent" and chat_message_info.is_group_chat_message:
            if "calendar_event" in entities:
                self.current_group_route["event_route"] = True
                self.current_group_route["event_name"] = entities["calendar_event"]
            else:
                self.current_group_route["location"] = current_destination

            self.current_group_route["current"] = current_location
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="user_request")
            self.state_machine.plan_group_route()

        if intent == "weather_intent":
            temperature, weather_description = self.weather.get_weather(self.chatbot_delegator.context.get_queried_location())
            text_data = {"temperature": temperature, "weather_description": weather_description,
                         "location": self.chatbot_delegator.context.get_queried_location()}
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="weather", text_data=text_data)
        if intent == "fuel_distance_intent":
            fuel_distance_state = self.car.get_fuel_distance()
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="fuel_distance", text_data=fuel_distance_state)
        if intent == "windows_question_intent":
            windows_state = self.car.get_windows()
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="windows_question", text_data=windows_state)
        if intent == "doors_question_intent":
            doors_state = self.car.get_doors()
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="doors", text_data=doors_state)
        if intent == "car_position_intent":
            position_data = self.car.get_position()
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="car_position", text_data=position_data)
        if intent == "greet":
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="greet")
        if intent == "distance_intent":
            distance = self.car.get_distance_route([current_location, current_destination])
            duration_seconds = self.car.get_duration_route([current_location, current_destination])
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="distance",
                                               text_data={"distance": distance, "duration_seconds": duration_seconds,
                                                "location": current_destination})
        return None

    # For recognized calendar_event in user message search calendar for the calendar_event. If found plan a route with
    # the extracted location from event in gcalendar.
    def plan_event_route(self, chat_message_info,current_location, calendar_event):
        events = self.calendar.get_events()
        if not events:
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="no_event")
        for event in events:
            if calendar_event.lower() in event["summary"].lower():
                start = event['start'].get('dateTime', event['start'].get('date'))
                des = event.get("description", None)
                print(start, event['summary'], event['location'], des)
                text_data = {"start_time": start, "location": event['location'], "summary": event['summary'],
                             "description": des}
                self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="event", text_data=text_data)
                self.plan_route(chat_message_info, current_location, event['location'], time=start)

    def plan_route(self, chat_message_info, current_location, current_destination, time=None):
        waypoints = [current_location, current_destination]
        traveling_time_seconds = self.car.get_duration_route(waypoints)
        route_id = self.save_route(waypoints)  # to identify which route to be planned when user answers
        self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="send_action",
                                           text_data={"action_type": "upload_photo"})
        # get Image
        download_status = self.car.get_route_image(waypoints)
        if download_status:
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="route_image",
                                               text_data="Route nach " + current_destination + ". Fahrtzeit: "
                                               + self.chatbot_delegator.nlg.human_readable_time(traveling_time_seconds))
        self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="send_action", text_data={"action_type": "typing"})
        self.chatbot_delegator.send_user_route_query(route_id, chat_message_info=chat_message_info)

    def plan_group_route(self,chat_message_info):
        waypoints = []
        waypoints.append(self.current_group_route["current"])
        waypoints.extend(self.current_group_route["dest"])
        if self.current_group_route["event_route"]:
            events = self.calendar.get_events()
            for event in events:
                if self.current_group_route["event_name"].lower() in event["summary"].lower():
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    des = event.get("description", None)
                    print(start, event['summary'], event['location'], des)
                    text_data = {"start_time": start, "location": event['location'], "summary": event['summary'],
                                 "description": des}
            waypoints.append(text_data["location"])
            self.current_group_route["location"] = text_data["location"]
        else:
            waypoints.append(self.current_group_route["location"])

        self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="send_action",
                                           text_data={"action_type": "upload_photo"})
        # get Image
        traveling_time_seconds = self.car.get_duration_route(waypoints)

        download_status = self.car.get_route_image(waypoints)
        if download_status:
            self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="route_image",
                                               text_data="Route nach " + self.current_group_route["location"] + ". Fahrtzeit: "
                                                         + self.chatbot_delegator.nlg.human_readable_time(
                                                   traveling_time_seconds))
        status = self.car.send_route_to_car(waypoints)
        self.chatbot_delegator.sendMessage(chat_message_info=chat_message_info, message_type="send_action", text_data={"action_type": "typing"})

        if status:
            self.chatbot_delegator.sendMessage(chat_message_info, message="Route wurde an das Navigationsystem gesendet.")
        self.current_group_route = {"event_route": False, "current": "", "location": "", "event_name": "", "dest": []}



    def save_route(self, waypoints):
        self.route_id += 1
        self.savedRoutes[self.route_id] = waypoints
        return self.route_id

    # get saved route and sent it
    def send_route_to_car(self, route_id):
        status = self.car.send_route_to_car(self.savedRoutes[route_id])
        return status

    def shutdown(self):
        self.scheduler.shutdown(wait=False)
        print "Shutting Down Actions"

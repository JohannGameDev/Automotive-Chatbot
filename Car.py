import requests
import json
import shutil
import config


class Car(object):
    def __init__(self):
        self.VIN_CAR = config.VIN_CAR  # vin of car

    # Calculae a route
    # PARAM: list of waypoints of route starting with start location end with end location
    def calculate_route(self, waypoints):
        r = requests.post("http://127.0.0.1:8000/api/routes", json={"routePoints": waypoints})
        route_data = r.json()
        return route_data

    def get_duration_route(self, waypoints):
        route_data = self.calculate_route(waypoints)
        traveling_time_seconds = route_data.get("durationSeconds", None)
        return traveling_time_seconds

    def get_distance_route(self, waypoints):
        route_data = self.calculate_route(waypoints)
        distance = route_data.get("distanceKilometers", None)
        return distance

    def get_departure_route(self, waypoints):
        route_data = self.calculate_route(waypoints)
        traveling_time_seconds = route_data.get("durationSeconds", None)
        return traveling_time_seconds

    # saves route images to images/img.png
    def get_route_image(self, waypoints):
        route_data = self.calculate_route(waypoints)
        route_map_url = route_data.get("routeMapUrl", None)
        try:
            response = requests.get(route_map_url, stream=True)
            with open('images/img.png', 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            return True
        except:
            print "Couldn't download Route Image."
            return False

    def send_route_to_car(self, waypoints):
        print "The waypoints of the route that you about to send are: "
        print waypoints
        route_data = self.calculate_route(waypoints)
        destination = route_data.get("geocodedWaypoints", None)[
            1]  # take destination with an location json to feed to car
        r = requests.post("http://127.0.0.1:8000/api/cars/"+self.VIN_CAR+"/destinations", json=destination)
        if r.status_code == 200 and destination != None:
            return True
        else:
            return False

    def get_car_status(self):
        r = requests.get("http://127.0.0.1:8000/api/cars/" + self.VIN_CAR + "/status")
        status_data = r.json()
        return status_data

    def get_fuel_distance(self):
        car_status = self.get_car_status()
        fuel_data = car_status["fuel"]
        fuel_percentage = fuel_data["percentage"]
        fuel_state = fuel_data["state"]
        range_data = car_status["range"]
        range_state = range_data["total"]["state"]
        range_distance = range_data["total"]["kilometers"]
        fuel_distance_state = {"fuel_percentage": fuel_percentage, "fuel_state": fuel_state, "range_state": range_state,
                               "range_distance": range_distance}
        return fuel_distance_state

    def get_position(self):
        r = requests.get("http://127.0.0.1:8000/api/cars/" + self.VIN_CAR + "/position")
        position_data = r.json()
        address_line = position_data["location"]["addressLine"]
        coordinates = {"latitude": position_data["location"]["coordinates"]["latitude"],
                       "longitude": position_data["location"]["coordinates"]["longitude"]}
        links = {"image_url": position_data["location"]["links"]["imageUrl"],
                 "map_url": position_data["location"]["links"]["mapUrl"]}
        return {"coordinates": coordinates, "address_line": address_line, "links": links}

    def get_windows(self):
        windows_data = self.get_car_status()["windows"]
        windows_list = ["doorFrontLeft", "doorFrontRight", "doorRearLeft", "doorRearRight"]
        windows = {}
        for window in windows_list:
            window_data = windows_data[window]
            window_dictionary = {"state": window_data["state"], "percentage": window_data["percentage"],
                                 "capture_date": window_data["captureDate"]}
            windows[window] = window_dictionary
        windows_state_data = {"front_left": windows["doorFrontLeft"]["state"],
                              "front_right": windows["doorFrontRight"]["state"],
                              "rear_left": windows["doorRearLeft"]["state"],
                              "rear_right": windows["doorRearRight"]["state"]}

        return windows_state_data

    def get_doors(self):
        doors_data = self.get_car_status()["doors"]
        doors_list = ["frontLeft", "frontRight", "rearLeft", "rearRight", "hood", "trunk"]
        doors = {}
        for door in doors_list:
            door_data = doors_data[door]
            doors[door] = {"closed_state": door_data["closedState"], "locked_state": door_data["lockedState"]}

        return doors

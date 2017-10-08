class Context(object):
    def __init__(self,current_location="Carnotstr. 4"):
        self.intent_history = []
        self.entities_history = []
        self.destination_location_history = []
        self.current_location_history = []
        self.current_location = current_location
        self.last_location = ""
        self.last_destination = ""
        self.current_destination = ""
        self.queried_location = current_location

    def set_current_destination(self,current_destination):
        self.destination_location_history.append(self.last_destination)
        self.last_destination = self.current_destination
        self.current_destination = current_destination

    def set_current_location(self,current_location):
        self.current_location_history.append(self.last_location)
        self.last_location = self.current_location
        self.current_location = current_location

    def get_queried_location(self):
        print self.queried_location
        return self.queried_location

    def update_queried_location(self,location):
        print location
        self.queried_location = location

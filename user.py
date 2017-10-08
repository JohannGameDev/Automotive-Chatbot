from tinydb import TinyDB, Query

class User(object):

    def __init__(self):
        self.db = TinyDB("user_db.json")
        self.user_query = Query()


    def is_existing_user(self,user_chat_id):
        if self.db.contains(self.user_query.user_chat_id == user_chat_id) > 0:
            return True
        else:
            return False

    def add_user(self, user_chat_id, name, address):
        self.db.insert({"user_chat_id":user_chat_id, "user_name":name, "user_address": address})

    def get_user_address(self,user_chat_id):
        return self.db.get(self.user_query.user_chat_id == user_chat_id).get("user_address")


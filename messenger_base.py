import abc


class MessengerServiceBase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self,messenger):
        self.mal = messenger

    @abc.abstractmethod
    def hear(self):
        """ Call when user sends a message"""
        return

    @abc.abstractmethod
    def emit(self,user_id,message):
        """ Send message to specifc user by userguide """
        return
    @abc.abstractmethod
    def start_service(self):
        """ starts the specific implementation """
        return

class AbstractMessage(object):
    MESSAGE_TYPE_DECISION = 0 # Let the user make specifc decisions
    MESSAGE_TYPE_MESSAGE = 1 # Write a normal message to user
    MESSAGE_TYPE_CALLBACK = 2  # Callback from user decision
    MESSAGE_TYPE_CALLBACK_ANSWER = 2 # answer a callback typicly answer on decision
    MESSAGE_TYPE_POSITION = 3 #Send a long/lat position
    MESSAGE_TYPE_ROUTE_IMAGE = 4 # send an image to an user
    MESSAGE_TYPE_SEND_ACTION = 5 # display an action status to the user


    """ decision in from of decisions= {"decision1": "callback_data","decision2:"callback_data" }"""
    """ data that comes from a callback usually after a decision was send to the user, callback_data={"route_id":x,callbackId:y,userChoice:z,chat_id: id "} """
    """ callback_aswer -  answer to an callback after the usser got decions a callback was fired and then we have to answer the callback callback_aswer:{"callback_id":callback_id,"callback_text":callback_text",additional_massage=additional_message}"""
    """ position data to {coordinates ,mapurl , imageurl} """
    def __init__(self,message_type=0,message="Default Message",decisions=None,callback_data=None,callback_answer=None,position_data=None,image_caption=None,action_type=""):
        self.message = message
        self.message_type = message_type
        self.decisions = decisions
        self.callback_data = callback_data
        self.callback_answer = callback_answer
        self.position_data = position_data
        self.image_caption = image_caption
        self.action_type = action_type

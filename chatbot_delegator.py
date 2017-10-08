# -*- coding: utf-8 -*-

from Nlu import Nlu
from Nlg import Nlg
from Actions import Actions
from messenger_base import AbstractMessage
from context import Context


class ChatbotDelegator(object):
    def __init__(self, mal):
        self.context = Context()
        self.nlg = Nlg()
        self.nlu = Nlu(self.context)
        self.mal = mal
        self.actions = Actions(self)

    def send_user_route_query(self, route_id, message_type=None, text_data=None, chat_message_info=""):
        self.mal.sendMessage(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_DECISION,
                                                                message="Die Route an den Boardcomputer senden?",
                                                                decisions={
                                                                "Ja": "route_id:" + str(route_id) + ";decision:true",
                                                                "Nein": "route_id:" + str(
                                                                    route_id) + ";decision:false"}))

    def sendMessage(self, chat_message_info="", message="", message_type=None, text_data=None):
        if message_type == "car_position":
            self.mal.sendMessage(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_POSITION,
                                                                    position_data=text_data))
        elif message_type == "route_image":
            self.mal.sendMessage(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_ROUTE_IMAGE,
                                                                    image_caption=text_data))
        elif message_type == "send_action":
            self.mal.sendMessage(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_SEND_ACTION,
                                                                    action_type=text_data["action_type"]))
        else:
            self.mal.sendMessage(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_MESSAGE,
                                                                    message=self.nlg.create_message(message=message,
                                                                                                message_type=message_type,
                                                                                                text_data=text_data)))

    def process_callback(self,chat_message_info, message):
        callback_id = message.callback_data["callback_id"]
        if message.callback_data["user_choice"] == "true":
            success = self.actions.send_route_to_car(message.callback_data["route_id"])
            if success:
                self.mal.sendMessage(chat_message_info,
                                     AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_CALLBACK_ANSWER,
                                                           callback_answer={"callback_id": callback_id,
                                                                            "callback_text": "Gesendet",
                                                                            "additional_massage": "Route wurde an das Auto gesendet."}))
            else:
                self.mal.sendMessage(chat_message_info,
                                     AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_CALLBACK_ANSWER,
                                                           callback_answer={"callback_id": callback_id,
                                                                            "callback_text": "Fehler",
                                                                            "additional_massage": "Fehler"}))
        else:
            self.mal.sendMessage(chat_message_info,
                                 AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_CALLBACK_ANSWER,
                                                       callback_answer={"callback_id": callback_id,
                                                                        "callback_text": "Nicht gesendet",
                                                                        "additional_massage": "Du kannst die selbe Route später an das Auto schicken."}))

    def processMessage(self, chat_message_info="", message=""):
        if message.message_type == AbstractMessage.MESSAGE_TYPE_MESSAGE:
            intent, entities, confidence = self.nlu.parse_massage(message.message)
            #self.debug_bad(chat_message_info, message.message, intent, entities, confidence)
            self.actions.predict_action(intent, entities, confidence, chat_message_info=chat_message_info)
        if message.message_type == AbstractMessage.MESSAGE_TYPE_CALLBACK:
            self.process_callback(chat_message_info,message)

    def debug_bad(self, chat_message_info, message, intent, entities, confidence):
        conf = str(confidence)
        debug_message = u"[Debug] Message: {message} ; Intent: {intent} ; Entities: {entities} ; Confidence: {conf}".format(
            message=message, intent=intent, entities=str(entities), conf=conf)
        self.sendMessage(chat_message_info=chat_message_info, message=debug_message)

    def shutdown(self):
        self.actions.shutdown()
        print "Shutting down Chatbot."

from chatbot_delegator import ChatbotDelegator
from telegram_service import TelegramService

class MAL(object):
    def __init__(self):
        self.chatbot_delegator = ChatbotDelegator(self)
        self.messenger_services = {}
        self.registerService(TelegramService(self))

    def hear(self, chat_message_info, message):
        self.chatbot_delegator.processMessage(chat_message_info, message)

    def sendMessage(self,chat_message_info,message):
        service_name = chat_message_info.service_name
        self.messenger_services[service_name].emit(chat_message_info,message)

    def start_services(self):
        for messenger_service in self.messenger_services.values():
            messenger_service.start_service()

    def registerService(self,service):
        self.messenger_services[service.SERVICE_NAME] = service

    def shutdown(self):
        self.chatbot_delegator.shutdown()

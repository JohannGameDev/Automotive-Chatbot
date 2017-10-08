import abc
import telepot
import telepot.api
import urllib3
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from SpeechToText import SpeechToText
from os import path
import os
import config
from messenger_base import MessengerServiceBase
from messenger_base import AbstractMessage
from chat_message_info import ChatMessageInfo


#CARE FOR CHAT ID FROM TELEGRAM AND INTERNAL USER ID
class TelegramService(MessengerServiceBase):
        def __init__(self, mal):
            self.mal = mal
            self.SERVICE_NAME = "telegram"
            MessengerServiceBase.__init__(self, mal)
            self.TOKEN = config.TELEGRAM_BOT_TOKEN
            self.myproxy_url = config.PROXY_URL
            self.telegram_bot = telepot.Bot(self.TOKEN)

        def hear(self,msg):
            print msg
            is_group_chat = False
            group_chat_id = None

            x = content_type, chat_type, chat_id = telepot.glance(msg)
            content_type, chat_type, chat_id = x
            if chat_type == "group":
                is_group_chat = True
                group_chat_id = msg["chat"]["id"]

            chat_message_info = ChatMessageInfo(self.SERVICE_NAME,msg["from"]["id"],is_group_chat, group_chat_id,msg["from"]["first_name"])

            if content_type == "voice":
                file_id = msg.get("voice").get("file_id")
                chat_id = msg.get("chat").get("id")
                self.telegram_bot.sendChatAction(chat_id,"record_audio")
                print file_id
                print chat_id
                audio_succes = self.download_audio(file_id)
                if audio_succes:
                    speech_to_text = SpeechToText()
                    message = speech_to_text.get_text_from_speech()

                    if message != None:
                        self.mal.hear(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_MESSAGE, message=message))
                    else:
                        print "No message detected"
                else:
                    print "Could not download file"

            else:

                self.mal.hear(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_MESSAGE, message=msg["text"]))

        def emit(self,chat_message_info,message):

            if chat_message_info.is_group_chat_message:
                chat_id = chat_message_info.group_chat_id
            else:
                chat_id = chat_message_info.user_message_id

            if message.message_type == AbstractMessage.MESSAGE_TYPE_MESSAGE:
                self.telegram_bot.sendMessage(chat_id,message.message)
            if message.message_type == AbstractMessage.MESSAGE_TYPE_DECISION:
                decisions = []
                for decision in message.decisions.keys():
                    decisions.append([InlineKeyboardButton(text=decision,callback_data=message.decisions[decision])])
                print decisions
                keyboard = InlineKeyboardMarkup(inline_keyboard=decisions)
                self.telegram_bot.sendMessage(chat_id,message.message, reply_markup=keyboard)
            if message.message_type == AbstractMessage.MESSAGE_TYPE_CALLBACK_ANSWER:
                self.telegram_bot.answerCallbackQuery(message.callback_answer["callback_id"], text=message.callback_answer["callback_text"])
                self.telegram_bot.sendMessage(chat_id, message.callback_answer["additional_massage"])
            if message.message_type == AbstractMessage.MESSAGE_TYPE_POSITION:
                print message.position_data["coordinates"]["latitude"]
                print message.position_data["coordinates"]["longitude"]
                self.telegram_bot.sendLocation(chat_id,message.position_data["coordinates"]["latitude"],message.position_data["coordinates"]["longitude"])
            if message.message_type == AbstractMessage.MESSAGE_TYPE_ROUTE_IMAGE:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                rel_path = u"images/img.png"# unicode for right path but works without it too
                abs_file_path = os.path.join(script_dir, rel_path)
                route_image_file = open(abs_file_path,"rb")# only read bytes workes for images
                self.telegram_bot.sendPhoto(chat_id,route_image_file,caption=message.image_caption)
            if message.message_type == AbstractMessage.MESSAGE_TYPE_SEND_ACTION:
                self.telegram_bot.sendChatAction(chat_id,message.action_type)

        def on_callback_query(self,msg):

            query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
            chat_message_info = ChatMessageInfo(self.SERVICE_NAME,from_id)

            route_id,user_choice = self.parseQueryData(query_data)
            callback_data = {"callback_id":query_id,"route_id":route_id,"user_choice":user_choice}
            self.mal.hear(chat_message_info, AbstractMessage(message_type=AbstractMessage.MESSAGE_TYPE_CALLBACK, callback_data=callback_data))


        def parseQueryData(self,query_data):
            attributes = query_data.split(";")
            route_id = int(attributes[0].split(":")[1])
            decision = attributes[1].split(":")[1]
            return route_id,decision

        def start_service(self):
            telepot.api._pools = {
                'default': urllib3.ProxyManager(proxy_url = self.myproxy_url, num_pools = 3, maxsize = 10, retries = False, timeout = 30),
            }
            telepot.api._onetime_pool_spec = (urllib3.ProxyManager, dict(proxy_url = self.myproxy_url, num_pools = 1, maxsize = 1, retries = False, timeout = 30))

            self.telegram_bot.message_loop({'chat': self.hear,
                                            'callback_query': self.on_callback_query})
        def download_audio(self,file_id):
            try:
                script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
                rel_path = "telegram_audio/audio.ogg"
                abs_file_path = os.path.join(script_dir, rel_path)

                print('Downloading file from telegram ...')
                self.telegram_bot.download_file(file_id, abs_file_path)
            except:
                print('Error: Could not download audio')
                return False
            return True





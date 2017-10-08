class ChatMessageInfo(object):

    def __init__(self, service_name, user_message_id, is_group_chat_message=False,group_chat_id=None,user_name=None):
        self.service_name = service_name
        self.user_message_id = user_message_id
        self.is_group_chat_message = is_group_chat_message
        self.group_chat_id = group_chat_id
        self.user_name = user_name
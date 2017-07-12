from datetime import datetime

class Message(object):
    """docstring for Message."""

    def __init__(self, message_body, chat_room, author):
        super(Message, self).__init__()
        self.message_body = message_body
        self.message_date_stamp = datetime.now()
        self.chat_room = chat_room
        self.author = author

    # def get_message_body():
    #     return self.message_body
    #
    # def get_message_author():
    #     return self.author
    #
    # def get_message_date_stamp():
    #     return self.message_date_stamp
    #
    # def get_message_chat_room():
    #     return self.chat_room

    def __str__(self):
        return str(self.message_date_stamp) + str(self.author) + str(self.message_body)

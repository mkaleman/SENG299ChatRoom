from Chatroom import Chatroom
from Message import Message
from User import User

class Application(object):
    """docstring for Application."""

    def __init__(self):
        super(Application, self).__init__()
        self.users = []
        self.chatrooms = []

    def connect_client_to_server(self):

    def display_home_page(self):

    def display_help(self):

    def create_chatroom(self, chatroom_name):

    def delete_chatroom(self, chatroom_name):

    def display_chatrooms(self):
        for i in self.chatrooms:
            print i

    def convert_name_to_Chatroom(self, chatroom_name):

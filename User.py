class User(object):
    """docstring for User."""

    def __init__(self, alias, socket):
        super(User, self).__init__()
        self.alias = alias
        self.socket = socket
        self.room_owner = False

    def set_alias(self, new_alias):
        self.alias = new_alias

    def get_alias(self):
        return self.alias

    def get_socket(self):
        return self.socket

    def set_room_ownership(self, boolean):
        self.room_owner = boolean

    def get_room_ownership(self):
        return self.room_owner

    # def invite(self, alias, chatroom_name):
    #
    # def join(self, chatroom_name):
    #
    # def sendMessage(self, message_content, chatroom_name):
    #
    # def exit(self, chatroom_name):
    #
    # def convert_alias_To_User(self, alias):
    #
    # def convert_name_to_chatroom(self, chatroom_name):

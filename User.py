class User(object):
    """docstring for User."""


    def __init__(self, alias):
        super(User, self).__init__()
        self.alias = alias

    def set_alias(self, new_alias):
        self.alias = new_alias

    def get_alias(self):
        return self.alias

    def invite(self, alias, chatroom_name):

    def join(self, chatroom_name):

    def sendMessage(self, message_content, chatroom_name):

    def exit(self, chatroom_name):

    def convert_alias_To_User(self, alias):

    def convert_name_to_chatroom(self, chatroom_name):

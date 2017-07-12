class Chatroom(object):
    """docstring for Chatroom."""

    def __init__(self, room_name):
        super(Chatroom, self).__init__()
        self.room_name = room_name
        self.members = []
        self.blocked_users = []
        self.messages = []

    def block_user(self, alias):
        user = convert_alias_to_User(alias)
        if user in self.members:
            self.blocked_users.append(user)
            self.memebers.remove(user)
            print alias + " successfully blocked from chatroom " + self.room_name
        else:
            print "ERROR: Can't block " + alias + " as they are not currently a room member."

    def unblock_user(self, alias):
        user = convert_alias_to_User(alias)
        if user in self.blocked_users:
            self.blocked_users.remove(user)
            print alias + " successfully unblocked from chatroom " + self.room_name
        else:
            print "ERROR: Can't unblock " + alias + " as they are not currently blocked."

    def display_users(self, alias):
        for i in self.members:
            print i.get_alias()

    def display_messages(self):
        for i in self.messages:
            print i

    def convert_alias_to_User(self, alias):

    def __str__(self):
        return str(self.room_name)

class Chatroom(object):
    """docstring for Chatroom."""

    def __init__(self, room_name, creator):
        super(Chatroom, self).__init__()
        self.room_name = room_name
        self.members = []
        self.members.append(creator)
        self.active_members = []
        self.blocked_users = []
        self.messages = []

    def get_room_name(self):
        return self.room_name

    def get_owner(self):
        return self.members[0]

    def change_owner(self):
        del self.members[0]

    def add_member(self, user):
        self.members.append(user)

    def add_active_member(self, user):
        self.active_members.append(user)

    def get_active_members(self):
        return self.active_members

    def remove_active_member(self, user):
        if user in self.active_members:
            self.active_members.remove(user)

    # def block_user(self, alias):
    #     user = convert_alias_to_User(alias)
    #     if user in self.members:
    #         self.blocked_users.append(user)
    #         self.members.remove(user)
    #         print alias + " successfully blocked from chatroom " + self.room_name
    #     else:
    #         print "ERROR: Can't block " + alias + " as they are not currently a room member."
    #
    # def unblock_user(self, alias):
    #     user = convert_alias_to_User(alias)
    #     if user in self.blocked_users:
    #         self.blocked_users.remove(user)
    #         print alias + " successfully unblocked from chatroom " + self.room_name
    #     else:
    #         print "ERROR: Can't unblock " + alias + " as they are not currently blocked."
    #
    # def display_users(self, alias):
    #     for i in self.members:
    #         print i.get_alias()
    #
    # def display_messages(self):
    #     for i in self.messages:
    #         print i
    #
    # def convert_alias_to_User(self, alias):
    #
    # def __str__(self):
    #     return str(self.room_name)

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
        self.members.remove(self.get_owner())
        if len(self.members) != 0:
            self.members[0].set_room_ownership(True)

    def add_member(self, user):
        self.members.append(user)

    def add_active_member(self, user):
        self.active_members.append(user)

    def get_active_members(self):
        return self.active_members

    def remove_active_member(self, user):
        if user in self.active_members:
            self.active_members.remove(user)

    def get_members(self):
        return self.members

    def get_blocked_users(self):
        return self.blocked_users

    def block_user(self, user):
        if user in self.members:
            self.blocked_users.append(user)
            self.members.remove(user)
            self.active_members.remove(user)
            user.set_active_room(None)
            return True
        else:
            return False

    def unblock_user(self, user):
        if user in self.blocked_users:
            self.blocked_users.remove(user)
            return True
        else:
            return False

    def get_messages(self):
        text = ""
        for i in self.messages:
            text += i + "\n"
        return text

    def add_message(self, msg):
        self.messages.append(msg)
        if len(self.messages) > 100:
            self.messages.pop()

    def remove_user(self, user):
        owner_change = False
        if self.get_owner() == user:
            self.change_owner()
            owner_change = True
        if user in self.active_members:
            self.active_members.remove(user)
            for usr in self.active_members:
                usr.get_socket().send(user.get_alias() + " has left the application.")
        if user in self.members:
            self.members.remove(user)
        if user in self.blocked_users:
            self.blocked_users.remove(user)
        if len(self.members) == 0:
            return ""
        if owner_change:
            if len(self.members) == 0:
                return ""
            else:
                return self.members[0]
        else:
            return False

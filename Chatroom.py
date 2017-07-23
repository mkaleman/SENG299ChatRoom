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

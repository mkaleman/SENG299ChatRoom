from Chatroom import Chatroom

class User(object):
    """docstring for User."""

    def __init__(self, alias, socket):
        super(User, self).__init__()
        self.alias = alias
        self.socket = socket
        self.room_owner = False
        self.active_room = None
        self.response = None
        self.broadcast = True

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

    def set_active_room(self, room):
        self.active_room = room

    def get_active_room(self):
        return self.active_room

    def set_response(self, message):
        self.response = message

    def get_response(self):
        return self.response

    def set_broadcasting(self, boolean):
        self.broadcast = boolean

    def broadcasting(self):
        return self.broadcast

    # def request_to_join(self, user, room):
    #     self.socket.send("User %s has requested to join chatroom %s. Allow them to join? [Y,n]" % (user.get_alias(), room.get_room_name()))
    #     response = self.socket.recv(1024)
    #     if response == "y" or response == "Y":
    #         room.add_member(user)

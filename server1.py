import socket
from threading import Thread
from User import User
from Chatroom import Chatroom

class Server(object):
    """docstring for Server."""
    def __init__(self):
        super(Server, self).__init__()
        self.ROOM_LIST = []
        self.server_sock = socket.socket()
        self.HOST = '192.168.0.7'
        self.PORT = 8000
        self.server_sock.bind((self.HOST, self.PORT))


    def run(self):
        print 'Starting Chat Server...'
        self.server_sock.listen(5)
        print 'Server Listening...'
        Thread(target=self.accept_client).start()


    def get_rooms(self):
        msg = "CURRENT CHAT ROOMS: \n"
        for room in self.ROOM_LIST:
            msg += room.get_room_name()
            msg += "\n"
        return msg


    def accept_client(self):
        while True:
            client_sock, client_addr = self.server_sock.accept()
            uname = client_sock.recv(1024)
            new_user = User(uname, client_sock)
            print '%s is now connected' % uname
            new_user.get_socket().send(self.get_rooms())
            Thread(target=self.broadcast_usr, args=[new_user]).start()


    def create_room(self, rname, user):
        if len(self.ROOM_LIST) <= 20:
            if not [x for x in self.ROOM_LIST if x.get_room_name() == rname]:
                if user.get_room_ownership() == False:
                    new_room = Chatroom(rname, user)
                    self.ROOM_LIST.append(new_room)
                else:
                    user.get_socket().send("Can't create room: you have already created a room")
            else:
                user.get_socket().send("Can't create room: a room with name %s has already been created" % rname)
        else:
            user.get_socket().send("Can't create room: the maximum number of rooms has already been created.")


    def join_room(self, rname, user):
        for room in self.ROOM_LIST:
            if room.get_room_name() == rname:
                room.add_member(user)
                room.add_active_member(user)
                for i in room.get_active_members():
                    if i.get_socket() != user.get_socket():
                        i.get_socket().send("%s has joined the room." % user.get_alias())


    def exit(self, rname, user):
        for room in self.ROOM_LIST:
            if room.get_room_name() == rname:
                room.remove_active_member(user)
                for i in room.get_active_members():
                    if i.get_socket() != user.get_socket():
                        i.get_socket.send("%s has left the room." % user.get_alias())


    def help(self, user):
        text = "Commands and Their Functions: \n"
        text += "/help:\tdisplays a list of commands \n"
        text += "/create [chat room name]:\tallows you to create a new chat room of the specified name \n"
        text += "/join [chat room name]:\tallows you to join a chat room of the specified name \n"
        text += "/exit [chat room name]:\tallows you to exit the chat room"
        user.get_socket().send(text)


    def handle_command(self, text, user):
        if text[0] == "/create":
            self.create_room(text[1], user)
        elif text[0] == "/join":
            self.join_room(text[1], user)
        elif text[0] == "/exit":
            self.exit(text[1], user)
        else:
            self.help(user)


    def broadcast_usr(self, user):
        while True:
            try:
                data = user.get_socket().recv(1024)
                if data:
                    text = data
                    text = text.split()
                    if text[0][0] == '/':
                        self.handle_command(text, user)
                    else:
                        r_index = 0
                        count = 0
                        for room in self.ROOM_LIST:
                            if user in room.get_active_members():
                                self.b_usr(user, data, room)
            except Exception as x:
                print(x.message)
                break


    def b_usr(self, user, msg, room):
        for i in room.get_active_members():
            if i.get_socket() != user.get_socket():
                i.get_socket().send(user.get_alias() + ": " + msg)

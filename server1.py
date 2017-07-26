import socket
from threading import Thread
from User import User
from Chatroom import Chatroom
from datetime import datetime

class Server(object):
    """docstring for Server."""

    def __init__(self):
        super(Server, self).__init__()
        self.ROOM_LIST = []
        self.USER_LIST = []
        self.server_sock = socket.socket()
        self.HOST = 'localhost'
        self.PORT = 8000
        self.server_sock.bind((self.HOST, self.PORT))


    def run(self):
        print 'Starting Chat Server...'
        self.server_sock.listen(5)
        print 'Server Listening...'
        Thread(target=self.accept_client).start()


    def get_rooms(self):
        if self.ROOM_LIST:
            msg = "CURRENT CHAT ROOMS: \n"
            for room in self.ROOM_LIST:
                msg += room.get_room_name()
                msg += "\n"
            return msg
        else:
            return "No rooms have been created yet"


    def valid_username(self, uname):
        if not [x for x in self.USER_LIST if x.get_alias() == uname]:
            return True
        else:
            return False


    def accept_client(self):
        while True:
            client_sock, client_addr = self.server_sock.accept()
            uname = client_sock.recv(1024)
            while not self.valid_username(uname):
                client_sock.send("Username %s is already in use, please enter another: " % uname)
                uname = client_sock.recv(1024)
            new_user = User(uname, client_sock)
            self.USER_LIST.append(new_user)
            print '%s is now connected' % uname
            self.help(new_user)
            new_user.get_socket().send(self.get_rooms())
            Thread(target=self.broadcast_usr, args=[new_user]).start()


    def create_room(self, rname, user):
        if len(self.ROOM_LIST) <= 20:
            if not [x for x in self.ROOM_LIST if x.get_room_name() == rname]:
                if user.get_room_ownership() == False:
                    new_room = Chatroom(rname, user)
                    self.ROOM_LIST.append(new_room)
                    user.get_socket().send("Created chat room %s..." % rname)
                    new_room.members.append(user)
                    new_room.active_members.append(user)
                    user.set_active_room(new_room)
                    user.get_socket().send("Entering chat room %s..." % rname)
                else:
                    user.get_socket().send("Can't create room: you have already created a room")
            else:
                user.get_socket().send("Can't create room: a room with name %s has already been created" % rname)
        else:
            user.get_socket().send("Can't create room: the maximum number of rooms has already been created.")


    def join_room(self, rname, user):
        a = [x for x in self.ROOM_LIST if x.get_room_name() == rname]
        if a:
            room = a[0]
            if user in room.get_blocked_users():
                user.get_socket().send("Can't enter room %s: You have been blocked from the room" % rname)
            elif user not in room.get_members():
                user.get_socket().send("Request to join room %s sent to room owner" % rname)
                owner = room.get_owner()
                owner.set_broadcasting(False)
                owner.get_socket().send("User %s has requested to join chatroom %s. Allow them to join? [Y,n]" % (user.get_alias(), rname))
                while not owner.broadcasting():
                    if owner.get_response():
                        if owner.get_response().lower() == "y" or owner.get_response().lower() == "n":
                            owner.set_broadcasting(True)
                        else:
                            owner.get_socket().send("Please enter 'Y' or 'n'")
                            owner.set_response(None)
                if owner.get_response().lower() == "y":
                   owner.get_socket().send("Successfully added %s to chat room" % user.get_alias())
                   room.add_member(user)
                if owner.get_response().lower() == "n":
                    owner.get_socket().send("Denied access to %s." % user.get_alias())
                    user.get_socket().send("Join request declined.")
                owner.set_response(None)
            if user in room.get_members():
                room.add_active_member(user)
                user.set_active_room(room)
                user.get_socket().send("Entering Room %s..." % rname)
                user.get_socket().send(room.get_messages())
                self.broadcast(user, "%s has joined the room." % user.get_alias(), room, False)
        else:
            user.get_socket().send("Can't enter room: Invalid room name.")


    def exit(self, user):
        if user.get_active_room():
            user.get_active_room().remove_active_member(user)
            self.broadcast(user, "%s has left the room." % user.get_alias(), user.get_active_room(), False)
            user.set_active_room(None)
            self.help(user)
            user.get_socket().send(self.get_rooms())
        else:
            user.get_socket().send("Are you sure you want to quit CMDirect? [Y/n]")
            response = user.get_socket().recv(1024)
            if response == "Y" or response == "y":
                user.get_socket().shutdown(1)
                user.get_socket().close()
                return False


    def help(self, user):
        text = "CMDirect\n\nCommands and Their Functions: \n"
        text += "/help:\t\t\t Display this message again. \n"
        text += "/create [room name]:\t Create a new chat room of the specified name. \n"
        text += "/delete [room name]:\t Delete the chat room.\n\t\t\t You must be the creator of the chatroom. \n"
        text += "/join [room name]:\t Join  the chat room. \n"
        text += "/invite [alias] [room]:\t Add alias to the chat room. \n"
        text += "/exit:\t\t\t Exit the current chat room or application. \n"
        text += "/set_alias [new_alias]:\t Change your alias. \n"
        text += "/display_users:\t\t Displays all active users of a room \n"
        text += "/display_rooms:\t\t Displays all active chat rooms \n"
        text += "/block [user]:\t\t Removes user from current chat room.\n\t\t\t You must be the creator of the chat room.\n"
        text += "/unblock [user]:\t Unblocks the user from the current chat room.\n\t\t\t You must be the creator of the chat room. \n\n"
        user.get_socket().send(text)


    def display_users(self, user):
        msg = "Current Users of "
        if user.get_active_room():
            msg += user.get_active_room().get_room_name() + "\n"
            for client in user.get_active_room().get_active_members():
                msg += client.get_alias() + "\n"
        else:
            msg += "CMDirect\n"
            for i in self.USER_LIST:
                msg += i.get_alias() + "\n"
        user.get_socket().send(msg)


    def display_rooms(self, user):
        user.get_socket().send(self.get_rooms())


    def set_alias(self, user, new_alias):
        if self.valid_username(new_alias):
            user.set_alias(new_alias)
            user.get_socket().send("Alias changed to %s" % new_alias)
        else:
            user.get_socket().send("Can't change alias: The alias you entered is already in use")


    def get_user_by_alias(self, alias):
        for i in self.USER_LIST:
            if i.get_alias() == alias:
                return i
        return None


    def get_room_by_room_name(self, room_name):
        for i in self.ROOM_LIST:
            if i.get_room_name() == room_name:
                return i
        return None


    def block(self, user, alias_to_block):
        user_to_block = self.get_user_by_alias(alias_to_block)
        room = user.get_active_room()
        if room:
            if room.get_owner() == user:
                if room.block_user(user_to_block):
                    user.get_socket().send("Successfully blocked %s from chat room %s" % (user_to_block.get_alias(), room.get_room_name()))
                    msg = "User %s has been blocked from the chat room" % user_to_block.get_alias()
                    self.broadcast(user, msg, room, False)
                    user_to_block.get_socket().send("You have been blocked from the chat room %s" % room.get_room_name())
                else:
                    user.get_socket().send("Can't block %s: They are not a member of %s" % (user_to_block.get_alias(), room.get_room_name()))
            else:
                user.get_socket().send("You must be the owner of a chat room to block a user")
        else:
            user.get_socket().send("You must be in a chat room to block a user")


    def unblock(self, user, alias_to_unblock):
        user_to_unblock = self.get_user_by_alias(alias_to_unblock)
        room = user.get_active_room()
        if room:
            if room.get_owner() == user:
                if room.unblock_user(user_to_unblock):
                    user.get_socket().send("Successfully unblocked %s from chat room %s" % (user_to_unblock.get_alias(), room.get_room_name()))
                    msg = "User %s has been unblocked from the chat room %s", (user_to_unblock.get_alias(), room.get_room_name())
                    self.broadcast(user, msg, room, False)
                    user_to_unblock.get_socket().send("You have been unblocked from the chat room %s" % room.get_room_name())
                else:
                    user.get_socket().send("Cant unblock %s: They are not currently blocked from chat room %s" % (user_to_unblock.get_alias(), room.get_room_name()))
            else:
                user.get_socket().send("You must be the owner of a chat room to unblock a user")
        else:
            user.get_socket().send("You must be in a chat room to unblock a user")


    def invite(self, user, alias_to_invite, room_name):
        user_to_invite = self.get_user_by_alias(alias_to_invite)
        room = self.get_room_by_room_name(room_name)
        if room:
            if user_to_invite not in room.get_blocked_users():
                if user_to_invite not in room.get_members():
                    room.add_member(user_to_invite)
                    user.get_socket().send("Successfully added %s to %s" % (room.get_room_name(), alias_to_invite))
                    user_to_invite.get_socket().send("You have been added to the chat room %s by user %s" % (room.get_room_name(), user.get_alias()))
                else:
                    user.get_socket().send("Can't invite %s: They are already a member of the chat room %s" % (alias_to_invite, room.get_room_name()))
            else:
                user.get_socket().send("Can't invite %s: They are blocked from the chat room %s" % (alias_to_invite, room.get_room_name()))
        else:
            user.get_socket().send("Can't invite %s: Invalid room name" % alias_to_invite)


    def delete(self, user, room_name):
        room = self.get_room_by_room_name(room_name)
        if room:
            if room.get_owner() == user:
                self.broadcast(user, "The chat room %s has been deleted" % room_name, room, False)
                for i in room.get_active_members():
                    i.set_active_room(None)
                self.ROOM_LIST.remove(room)
                user.get_socket().send("Successfully deleted room %s" % room_name)
            else:
                user.get_socket().send("Can't delete room %s: You must be the owner of the room to delete it" % room_name)
        else:
            user.get_socket().send("Can't delete room %s: Invalid room name" % room_name)



    def handle_command(self, text, user):
        if text[0] == "/create":
            self.create_room(text[1], user)
        elif text[0] == "/join":
            self.join_room(text[1], user)
        elif text[0] == "/exit":
            self.exit(user)
        elif text[0] == "/display_users":
            self.display_users(user)
        elif text[0] == "/display_rooms":
            self.display_rooms(user)
        elif text[0] == "/set_alias":
            self.set_alias(user, text[1])
        elif text[0] == "/block":
            self.block(user, text[1])
        elif text[0] == "/unblock":
            self.unblock(user, text[1])
        elif text[0] == "/invite":
            self.invite(user, text[1], text[2])
        elif text[0] == "/delete":
            self.delete(user, text[1])
        else:
            user.get_socket().send("Invalid Command")
            self.help(user)


    def broadcast_usr(self, user):
        while True:
            try:
                data = user.get_socket().recv(1024)
                if data and user.broadcasting():
                    text = data
                    text = text.split()
                    if text[0][0] == '/':
                        self.handle_command(text, user)
                    else:
                        if user.get_active_room():
                            self.broadcast(user, data, user.get_active_room(), True)
                        else:
                            user.get_socket().send("You must enter a chat room to send a message.")
                elif data and not user.broadcasting():
                    user.set_response(data)
            except Exception as x:
                print(x.message)
                user.get_socket().shutdown(1);
                user.get_socket().close()
                return False


    def broadcast(self, user, msg, room, boolean):
        if boolean:
            message = "[" + datetime.now().strftime("%m-%d %H:%M") + "] " + user.get_alias() + ": " + msg
            room.add_message(message)
        else:
            message = msg
        for i in room.get_active_members():
            if not i == user:
                i.get_socket().send(message)

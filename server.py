import socket
from threading import Thread


def get_rooms():
    msg = "CURRENT CHAT ROOMS: \n"
    for room in ROOM_LIST:
        msg += room
        msg += "\n"
    return msg


def accept_client():
    while True:
        client_sock, client_addr = server_sock.accept()
        uname = client_sock.recv(1024)
        CONNECTION_LIST.append((uname, client_sock))
        print '%s is now connected' % uname
        client_sock.send(get_rooms())
        Thread(target=broadcast_usr, args=[uname, client_sock]).start()


def create_room(rname):
    ROOM_LIST.append(rname)


def join_room(rname, uname, sock):
    count = 0
    for room in ROOM_LIST:
        if room == rname:
            LIST[count].append((uname, sock))
            for i in LIST[count]:
                if i[1] != sock:
                    i[1].send("%s has joined the room." % uname)
        count += 1


def exit(rname, uname, sock):
    count = 0
    for room in ROOM_LIST:
        if room == rname:
            LIST[count].remove((uname, sock))
            for i in LIST[count]:
                if i[1] != sock:
                    i[1].send("%s has left the room." % uname)
        count += 1


def help(uname, client_sock):
    text = "Commands and Their Functions: \n"
    text += "/help: displays a list of commands \n"
    text += "/create [chat room name]: allows you to create a new chat room of the specified name \n"
    text += "/join [chat room name]: allows you to join a chat room of the specified name \n"
    text += "/exit [chat room name]: allows you to exit the chat room"
    client_sock.send(text)


def handle_command(text, uname, client_sock):
    if text[0] == "/create":
        create_room(text[1])
    elif text[0] == "/join":
        join_room(text[1], uname, client_sock)
    elif text[0] == "/exit":
        exit(text[1], uname, client_sock)
    elif text[0] == "/help":
        help(uname, client_sock)


def broadcast_usr(uname, client_sock):
    while True:
        try:
            data = client_sock.recv(1024)
            if data:
                text = data
                text = text.split()
                if text[0] == "/create" or text[0] == "/join" or text[0] == "/exit" or text[0] == "/help":
                    handle_command(text, uname, client_sock)
                else:
                    r_index = 0
                    count = 0
                    for room in LIST:
                        for user in room:
                            if user[0] == uname:
                                r_index = count
                        count += 1
                    b_usr(uname, client_sock, data, r_index)
        except Exception as x:
            print(x.message)
            break


def b_usr(uname, sock, msg, r_index):
    for i in LIST[r_index]:
        if i[1] != sock:
            i[1].send(uname + ": " + msg)


CONNECTION_LIST = []
LIST = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
ROOM_LIST = []
server_sock = socket.socket()

HOST = 'localhost'
PORT = 8000
server_sock.bind((HOST, PORT))

server_sock.listen(5)
print "Chat server started.."

Thread(target=accept_client).start()

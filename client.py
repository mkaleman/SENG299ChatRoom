import socket
from threading import Thread
import sys


def send():
    while True:
        msg = raw_input('Me: ')
        client_sock.send(msg)


def receive():
    while True:
        data = client_sock.recv(1024)
        sys.stdout.write("\n" + str(data) + "\nMe:")
        sys.stdout.flush()


client_sock = socket.socket()

HOST = 'localhost'
PORT = 8000
client_sock.connect((HOST, PORT))
print 'Connected to Server.'
uname = raw_input('Enter your name: ')
client_sock.send(uname)
sys.stdout.write("Please join one of the available rooms: \n")

Thread(target=send).start()
Thread(target=receive).start()

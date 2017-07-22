import socket
from threading import Thread
import sys

class Client(object):
    """docstring for Client."""

    def __init__(self):
        super(Client, self).__init__()
        self.client_sock = socket.socket()
        self.HOST = '192.168.0.7'
        self.PORT = 8000
        self.client_sock.connect((self.HOST, self.PORT))

    def run(self):
        print 'Connected to Server...'
        self.uname = raw_input('Enter your name: ')
        self.client_sock.send(self.uname)
        sys.stdout.write("Please join one of the available rooms: \n")
        Thread(target=self.send).start()
        Thread(target=self.receive).start()

    def send(self):
        while True:
            msg = raw_input('Me: ')
            self.client_sock.send(msg)

    def receive(self):
        while True:
            data = self.client_sock.recv(1024)
            sys.stdout.write("\n" + str(data) + "\nMe:")
            sys.stdout.flush()

import socket
from threading import Thread


HOST = '192.168.122.1'
PORT = 8000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((HOST, PORT))
except:
    print 'Unable to connect...'

while True:
    message = raw_input("Your Message: ")
    s.send(message)

    if message == 'quit':
        break
#    print "Awaiting Reply"
#    reply = s.recv(1024)
#    print "Received ", repr(reply)

s.close()
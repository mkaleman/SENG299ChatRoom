import socket
from threading import Thread

def client_handler():
    conn, addr = s.accept()
    print addr, " joined the chat"
    while 1:
        data = conn.recv(1024)

        if not data:
            break

        print 'Received Message:', repr(data)

HOST = ''
PORT = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print 'Server is running...'

for i in range(20):
    Thread(target=client_handler).start()

s.close()

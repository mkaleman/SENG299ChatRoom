import socket
from threading import Thread

def accept_client():
	while True:
		client_sock, client_addr = server_sock.accept()
		uname = client_sock.recv(1024)
		CONNECTION_LIST.append((uname, client_sock))
		print '%s is now connected' % uname
		Thread(target=broadcast_usr, args=[uname, client_sock]).start()

def broadcast_usr(uname, client_sock):
	while True:
		try:
			data = client_sock.recv(1024)
			if data:
				b_usr(uname, client_sock, data)
		except Exception as x:
			print(x.message)
			break

def b_usr(uname, sock, msg):
	for i in CONNECTION_LIST:
		if i[1] != sock:
			i[1].send(uname + ": " + msg)

CONNECTION_LIST = []

server_sock = socket.socket()

HOST = 'localhost'
PORT = 8000
server_sock.bind((HOST, PORT))

server_sock.listen(5)
print "Chat server started.."

Thread(target=accept_client).start()

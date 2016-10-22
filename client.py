import socket
import os
from _thread import *

s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
chat_server="0:0:0:0:0:0:0:1" #127.0.0.1		0:0:0:0:0:0:0:1
port=5555
username = input("Enter your username:\n>>>")
try:
	s.connect((chat_server,port))
	print ("connected to:",chat_server)
	data = s.recv(2048)
	motd = 'Message of the day: ' + data.decode('utf-8')
	print(str(motd))
	s.send(str.encode(username))
except socket.error as e:
	print(e)
def send_messages():
	while True:
		client_message = input(">>>")
		if client_message == "quit":
			break
		else:
			s.send(str.encode(client_message))
	s.close()
def recieve_messages():
	while True:
		try:
			message_data = s.recv(2048)
			server_message = message_data.decode('utf-8')
			print (server_message)
		except ConnectionAbortedError as e:
			print (e)
			print("Disconnected from:", chat_server)
			break
	s.close()
try:
	start_new_thread(send_messages,())
	start_new_thread(recieve_messages,())
except _thread.error as te:
	print(te)
while True:
	pass



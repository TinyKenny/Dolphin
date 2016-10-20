import socket
import os
import _thread

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
chat_server="localhost" #jag är 10.164.137.191
port=5555				#K //Lukas
username = input("Username:") #se rad 15
try:
	s.connect((chat_server,port))
	print ("connected to:",chat_server)
	data = s.recv(2048)
	motd = 'Message of the day: ' + data.decode('utf-8')
	print(str(motd))
	s.send(str.encode("username:"+username)) #går det att fixa i servern så att den anger vem det var som skickade meddelandet?
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
		message_data = s.recv(2048)
		server_message = message_data.decode('utf-8')
		print (server_message)
	s.close()
try:
	_thread.start_new_thread(send_messages,())
	_thread.start_new_thread(recieve_messages,())
except _thread.error as te:
	print(te)
while True:
	pass



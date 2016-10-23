import socket
import os
import threading
#Yes, I know, none of the comments are in swedish. deal with it
def send_messages(): #the function that sends messages
	while True:
		client_message = input(">>>")
		if client_message == "quit": #ends the while-loop, go to line 52
			break
		else:
			s.send(str.encode(client_message))
	s.close()
	return
def recieve_messages(): #the function that recieves messages
	while True:
		try:
			message_data = s.recv(2048)
			server_message = message_data.decode('utf-8')
			print (server_message)
		except ConnectionAbortedError as e: #this will happen when the user enters "quit" or when the server is shut down
			print (e) #prints out the error that specifies how the connection was lost
			print("Disconnected from:", chat_server)
			os.system("pause")
			os._exit(1)
			break
	return
username = input("Enter your username:\n>>>")
if username == "root": #enables client developer mode
	developer_mode = True #Boolean that keeps track of wether developer mode is active or not
	valid_protocol = False #you haven't even entered a protocol yet! :P
	while valid_protocol == False:
		address_protocol = input("IP protocol? (IPv4 or IPv6)\n")
		if address_protocol.lower() == "ipv4":
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creates a socket object for IPv4
			valid_protocol = True #IPv4 is a valid protocol
		elif address_protocol.lower() == "ipv6":
			s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM) #creates a socket object for IPv6
			valid_protocol = True #IPv6 is a valid protocol
		else:
			print("Invalid network protocol")
	chat_server = input("IP address?\n")
	port = int(input("Port?\n"))
	username = input("Username on server?\n") #to make it possible to enable client dev mode without connecting as root
else: #default values
	developer_mode = False #self-explanatory
	chat_server="0:0:0:0:0:0:0:1" #server address
	port=5555 #server port
	s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM) #creates socket object for IPv6

try:
	s.connect((chat_server,port))
	print ("connected to:",chat_server)
	data = s.recv(2048) #recieve the message of the day
	motd = "Message of the day: " + data.decode('utf-8') #currently just a random quote
	print(str(motd))
	s.send(str.encode(username)) #inform the server of your username
except socket.error as e: #couldn't connect to given IP + port
	print(e)
	os.system("pause")
	os._exit(1)
finally:
	sender = threading.Thread(target=send_messages,daemon=0)
	reciever = threading.Thread(target=recieve_messages,daemon=0)
	sender.start()
	reciever.start()
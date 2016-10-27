import socket
import os
import threading

def send_messages(): #the function that sends messages
	while True:
		client_message = input(">>>")
		if client_message[0:1] == "-": #lauches command intepreter
			if client_message=="-quit":
				break
			elif client_message=="-help":
				for command, desc in command_dict.items():
					print(command +"\t" +desc)
				if developer_mode:
					print("ROOT COMMANDS:")
					for command, desc in root_command_dict.items():
						print(command + "\t" + desc)

			elif client_message[0:5]=="-kick":
				s.send(str.encode(client_message))

			elif client_message[0:11] == "-save prof ":
				print("command not implemented")

			elif client_message[0:10] == "-del prof ":
				print("command not implemented")

			elif client_message[0:11] == "-edit prof ":
				print("command not implemented")

			elif client_message[0:10] == "-view prof":
				print("command not implemented")

			else:
				print("Unknown command:"+client_message)
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
			if server_message=="root:-kick " + username:
				raise ConnectionError
		except ConnectionError as e: #this will happen when the user enters "quit" or when the server is shut down
			print(e)
			print("Disconnected from:", chat_server)
			break
	return

#s=socket
address_protocol="ipv4"
chat_server="localhost"
port=5555
username=""
developer_mode=0

command_dict={"-help":"\t\t\tview this page",
			  "-quit":"\t\t\texit program",
			  "-save prof [name]":"save profile settings as [name]",
			  "-del prof [name]":"delete profile [name]",
			  "-view prof":"\t\tviews your saver profiles",
			  "-edit prof [name]":"edit profile [name]"}

root_command_dict={"terminate":"\t\tterminates the server",
				   "-kick [username]":"kicks [username] from the server"}

if (input("Load profile or connect to an unsaved server?y/n")).lower() == 'y':
	print("not implemented yet")
	# Add code to import a profile  here
	os._exit(0)  # since no profile is selected, it is useless to try to connect
else:
	username = input("Enter your username:\n>>>")
	if username == "root":  # enables client developer mode
		developer_mode = True  # Boolean that keeps track of wether developer mode is active or not
		print("You are now root user (admin)")
		username = input("Username on server?\n")  # to make it possible to enable client dev mode without connecting as root

while True:
#		address_protocol = input("IP protocol? (IPv4 or IPv6)\n>>>")
		if address_protocol.lower() == "ipv4":
			s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			break #IPv4 is a valid protocol
		elif address_protocol.lower() == "ipv6":
			s=socket.socket(socket.AF_INET6, socket.SOCK_STREAM) #creates a socket object for IPv6
			break #IPv6 is a valid protocol
		else:
			print("Invalid network protocol")

#comment these away if you want to connect to 127.0.0.1:5555
#chat_server = input("IP address?\n>>>")
#port = int(input("Port?\n>>>")) #error will be raised if you enter a string, GUI will solve that

try:
	s.connect((chat_server,port))
	print ("Connected to:",chat_server+":"+str(port))
	s.send(str.encode("yay"))
	data = s.recv(2048) #recieve the message of the day
	print("Message of the day: " + str(data.decode('utf-8'))) #currently just a random quote
	s.send(str.encode(username)) #inform the server of your username
except socket.error as e: #couldn't connect to given IP + port
	print("Cound not connect to",chat_server+":"+str(port) + "\n" + str(e))
	os._exit(1)

sender = threading.Thread(target=send_messages,daemon=0)
reciever = threading.Thread(target=recieve_messages,daemon=0)
sender.start()
reciever.start()
sender.join()
reciever.join()

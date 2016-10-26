import socket
import os
import threading
import configparser

def send_messages(): #the function that sends messages
	while True:
		client_message = input(">>>")
		if client_message[0:1] == "/": #lauches command intepreter
			if client_message=="/quit":
				break
			elif client_message=="/help":
				for command, desc in command_dict.items():
					print(command +"\t" +desc)
				if developer_mode:
					print("ROOT COMMANDS:")
					for command, desc in root_command_dict.items():
						print(command + "\t" + desc)

			elif client_message[0:5]=="/kick":
				s.send(str.encode(client_message))

			elif client_message[0:11] == "/save prof ":
				print("command not implemented")

			elif client_message[0:10] == "/del prof ":
				print("command not implemented")

			elif client_message[0:11] == "/edit prof ":
				print("command not implemented")

			elif client_message[0:10] == "/view prof":
				print("command not implemented")

			else:
				print("Unknown command:"+client_message)
		else:
			s.send(str.encode(client_message))
	s.close()
	os._exit(0)

def recieve_messages(): #the function that recieves messages
	while True:
		try:
			message_data = s.recv(2048)
			server_message = message_data.decode('utf-8')
			if not server_message:
				raise ConnectionError #meddelandet är tomt, linux har lite svårt att fatta när det är dags att gå hem annars
			print (server_message)
			if server_message=="root:-kick " + username:
				raise ConnectionError
		except ConnectionError as e: #this will happen when the user enters "quit" or when the server is shut down
			print("Disconnected from:", chat_server)
			break
	return

chat_server="127.0.0.1"
port=5555
username=""
developer_mode=0
config = configparser.ConfigParser()
config.read("profiles.ini")
network_protocol=""


command_dict={"/help":"              view this page",
			  "/quit":"              exit program",
			  "/save prof [name]":"  save profile settings as [name]",
			  "/del prof [name]":"  delete profile [name]",
			  "/view prof":"          views your saver profiles",
			  "/edit prof [name]":"  edit profile [name]"}

root_command_dict={"terminate":"        terminates the server",
				   "-kick [username]":" kicks [username] from the server"}

print("Select a proile to use or select manual:")
print("* manual")
for n in config.sections():
	print("*", n)


profile = input(">>>")
if profile in config.sections():
	network_protocol = str(config[profile]["network_protocol"])
	if network_protocol=="IPv4":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	else:
		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	port = int(config[profile]["port"])
	chat_server = str(config[profile]["ip"])
	username = str(config[profile]["username"])

elif profile == "manual":
	username = input("Enter your username:\n>>>")
	if username == "root":  # enables client developer mode
		developer_mode = True  # Boolean that keeps track of wether developer mode is active or not
		print("You are now root user (admin)")
		username = input("Username on server?\n")  # to make it possible to enable client dev mode without connecting as root
	address_protocol = input("Enter IP protocol(IPv4 or IPv6):\n>>>")
	if address_protocol.lower() == "ipv4":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	elif address_protocol.lower() == "ipv6":
		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	chat_server=input("Enter server IP:\n>>>")
	port = int(input("Enter port:\n>>>"))

try:
	s.connect((chat_server,port))
	print ("Connected to:",chat_server+":"+str(port))
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
import socket
import os
import threading
import configparser

def command_interpreter(client_message):
	if client_message == "/quit":
		s.close()
		return 1

	elif client_message == "/help":
		for command, desc in command_dict.items():
			print(command + "\t" + desc)
		if developer_mode:
			print("ROOT COMMANDS:")
			for command, desc in root_command_dict.items():
				print(command + "\t" + desc)

	elif client_message[0:5] == "/kick":
		s.send(str.encode(client_message))
		pass

	elif client_message[0:11] == "/prof save ":
		configEditor = configparser.RawConfigParser()

		for profile in config.sections():#lägga till de gamla profilerna i den nya filen
			configEditor.add_section(profile)
			configEditor.set(profile, "ip", config[profile]["ip"])
			configEditor.set(profile, "port", config[profile]["port"])
			configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
			configEditor.set(profile, "username", config[profile]["username"])
			if developer_mode:
				configEditor.set(profile, "developer_mode", "True")

		#lägga till den nya profilen till filen
		prof_name=client_message[11:]
		configEditor.add_section(prof_name)
		configEditor.set(prof_name, "ip", chat_server)
		configEditor.set(prof_name, "port", str(port))
		configEditor.set(prof_name, "network_protocol", network_protocol)
		configEditor.set(prof_name, "username", username)
		if developer_mode:
			configEditor.set(prof_name, "developer_mode", "True")
		print("Done!")

		with open('profiles.ini', 'w') as new_configfile:
			configEditor.write(new_configfile)

	elif client_message[0:10] == "/prof del ":
		if not (client_message[11:] in config.sections()):
			print("No such profile:"+client_message[11:])
			return 0

		configEditor = configparser.RawConfigParser()

		for profile in config.sections():#lägga till de gamla profilerna i den nya filen
			if profile==client_message[10:]:
				continue
			configEditor.add_section(profile)
			configEditor.set(profile, "ip", config[profile]["ip"])
			configEditor.set(profile, "port", config[profile]["port"])
			configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
			configEditor.set(profile, "username", config[profile]["username"])
			if developer_mode:
				configEditor.set(profile, "developer_mode", "True")

			with open('profiles.ini', 'w') as new_configfile:
				configEditor.write(new_configfile)

	elif client_message[0:11] == "/prof edit ":
		if not (client_message[11:] in config.sections()):
			print("No such profile:"+client_message[11:])
			return 0

		configEditor = configparser.RawConfigParser()

		for profile in config.sections():  # lägga till de gamla profilerna i den nya filen
			if profile == client_message[11:]: #den som ska ändas har hittats
				print("Current name:"+profile)
				new_profile_name = input("Enter new name:\n>>>")
				configEditor.add_section(new_profile_name)
				print("Current IP:"+chat_server)
				configEditor.set(new_profile_name, "ip", input("Enter new IP addres:\n>>>"))
				print("Current port:" + str(port))
				configEditor.set(new_profile_name, "port", input("Enter new port:\n>>>"))
				print("Current network protocol:" + network_protocol)
				configEditor.set(new_profile_name, "network_protocol", input("Enter new network protocol:\n>>>"))
				print("Current username:" + username)
				configEditor.set(new_profile_name, "username", input("Enter new username:\n>>>"))
				if developer_mode:
					if not input("Enter new dev mode status(True/False)\n>>>") == "False":
						configEditor.set(new_profile_name, "developer_mode", True)
				continue

			configEditor.add_section(profile)
			configEditor.set(profile, "ip", config[profile]["ip"])
			configEditor.set(profile, "port", config[profile]["port"])
			configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
			configEditor.set(profile, "username", config[profile]["username"])
			if developer_mode:
				configEditor.set(profile, "developer_mode", "True")

			with open('profiles.ini', 'w') as new_configfile:
				print("added ", configEditor.sections())
				configEditor.write(new_configfile)

	elif client_message[0:10] == "/prof view":
		for profile in config.sections():
			print(profile +
				  (15 - len(profile)) * " " +
				  config[profile]["ip"] +
				  (13 - len(config[profile]["ip"])) * " " +
				  config[profile]["port"] +
				  (8 - len(config[profile]["port"])) * " " +
				  config[profile]["network_protocol"] +
				  (8 - len(config[profile]["network_protocol"])) * " " +
				  config[profile]["username"])


	else:
		print("Unknown command:" + client_message)

def send_messages(): #the function that sends messages
	while True:
		client_message = input(">>>")
		if client_message[0:1] == "/": #lauches command intepreter
			if command_interpreter(client_message):
				break
		else:
			s.send(str.encode(client_message))

def recieve_messages(): #the function that recieves messages
	try:
		while True:
			message_data = s.recv(2048)
			server_message = message_data.decode('utf-8')
			if not server_message:
				raise ConnectionError #meddelandet är tomt, linux har lite svårt att fatta när det är dags att gå hem annars
			print (server_message)
			if server_message=="root:-kick " + username:
				raise ConnectionError
	except ConnectionError as e: #this will happen when the user enters "quit" or when the server is shut down
		print("Disconnected from:", chat_server)

chat_server="127.0.0.1"
port=5555
username=""
developer_mode=0
config = configparser.ConfigParser()
config.read("profiles.ini")
network_protocol="null"

command_dict={"/help":"view this page",
			  "/quit":"              exit program",
			  "/prof save [name]":"  save profile settings as [name]",
			  "/prof del [name]":"  delete profile [name]",
			  "/prof view":"          views your saver profiles",
			  "/prof edit [name]":"  edit profile [name]"}

root_command_dict={"terminate":"        terminates the server",
				   "/kick [username]":" kicks [username] from the server"}

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
	developer_mode= config.getboolean(profile, "developer_mode", fallback=False)

elif profile == "manual":
	username = input("Enter your username:\n>>>")
	if username == "root":  # enables client developer mode
		developer_mode = True  # Boolean that keeps track of wether developer mode is active or not
		print("You are now root user (admin)")
		username = input("Username on server?\n")  # to make it possible to enable client dev mode without connecting as root
	network_protocol = input("Enter IP protocol(IPv4 or IPv6):\n>>>")
	if network_protocol.lower() == "ipv4":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		network_protocol = "IPv4"
	elif network_protocol.lower() == "ipv6":
		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		network_protocol = "IPv6"
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

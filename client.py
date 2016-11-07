import socket
import os
import threading
import configparser

def spacer(spaces, string):
	return (spaces - len(string)) * " "

def command_interpreter(client_message):
	if client_message == "/quit":
		print("Closing...")
		return 1

	elif client_message == "/help":
		for command, desc in command_dict.items():
			print(command + desc)
		s.send(str.encode(client_message))
		print(s.recv(2048).decode("utf-8"))
		if developer_mode:
			print("ROOT COMMANDS:")
			for command, desc in root_command_dict.items():
				print(command + desc)

	elif client_message[0:6] == "/save ":
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
		prof_name=client_message[6:]
		configEditor.add_section(prof_name)
		configEditor.set(prof_name, "ip", chat_server)
		configEditor.set(prof_name, "port", str(port))
		configEditor.set(prof_name, "network_protocol", network_protocol)
		configEditor.set(prof_name, "username", username)
		if developer_mode:
			configEditor.set(prof_name, "developer_mode", "True")

		with open('profiles.ini', 'w') as new_configfile:
			configEditor.write(new_configfile)
			config.read("profiles.ini")
			print("Done!")

	elif client_message[0:5] == "/del ":
		if not (client_message[5:] in config.sections()):
			print("No such profile:"+client_message[5:])
			return 0

		configEditor = configparser.RawConfigParser()

		for profile in config.sections():#lägga till de gamla profilerna i den nya filen
			if profile==client_message[5:]:
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
			config.read("profiles.ini") #detta fungerar inte, ingen aning om varför, kan inte hitta en lösning
			print("Done!")

	elif client_message[0:11] == "/edit -all ":
		if not (client_message[11:] in config.sections()):
			print("No such profile:"+client_message[16:])
			return 0

		configEditor = configparser.RawConfigParser()

		for profile in config.sections():  # lägga till profilerna i den nya filen
			if profile == client_message[11:]: #den som ska ändas har hittats
				print("Current name:"+profile)
				new_profile_name = input("Enter new name:\n>>>")
				configEditor.add_section(new_profile_name)
				print("Current IP:"+config[profile]["ip"])
				configEditor.set(new_profile_name, "ip", input("Enter new IP addres:\n>>>"))
				print("Current port:" + str(config[profile]["port"]))
				configEditor.set(new_profile_name, "port", input("Enter new port:\n>>>"))
				print("Current network protocol:" + config[profile]["network_protocol"])
				configEditor.set(new_profile_name, "network_protocol", input("Enter new network protocol:\n>>>"))
				print("Current username:" + config[profile]["username"])
				configEditor.set(new_profile_name, "username", input("Enter new username:\n>>>"))
				if developer_mode:
					if not input("Enter new dev mode status(True/False)\n>>>") == "False":
						configEditor.set(new_profile_name, "developer_mode", True)
			else: #detta var inte profilen som skulle ändras, lägger till den som den är i den nya filen
				configEditor.add_section(profile)
				configEditor.set(profile, "ip", config[profile]["ip"])
				configEditor.set(profile, "port", config[profile]["port"])
				configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
				configEditor.set(profile, "username", config[profile]["username"])
				try:
					if config[profile]["developer_mode"]:
						configEditor.set(profile, "developer_mode", "True")
				except KeyError as e:
					pass #profilen var ej developer, inget ska hända

		with open('profiles.ini', 'w') as new_configfile:
			configEditor.write(new_configfile)
			config.read("profiles.ini") #detta fungerar inte, ingen aning om varför, kan inte hitta en lösning

	elif client_message[0:6] == "/edit ":
		if not (client_message[6:] in config.sections()):
			print("No such profile:"+client_message[6:])
			return 0

		configEditor = configparser.RawConfigParser()

		for profile in config.sections():  # lägga till profilerna i den nya filen
			if profile == client_message[6:]: #den som ska ändas har hittats
				print("Current name:"+profile)
				new_profile_name = input("Enter new profile name:\n>>>")
				configEditor.add_section(new_profile_name)
				print("Current IP:"+config[profile]["ip"])
				configEditor.set(new_profile_name, "ip", input("Enter new IP addres:\n>>>"))
				configEditor.set(new_profile_name, "port", config[profile]["port"]) #sker auto
				configEditor.set(new_profile_name, "network_protocol", config[profile]["network_protocol"])#sker auto
				print("Current username:" + config[profile]["username"])
				configEditor.set(new_profile_name, "username", input("Enter new username:\n>>>"))
				try:
					if config[profile]["developer_mode"]:
						configEditor.set(new_profile_name, "developer_mode", "True")
				except KeyError as e:
					pass #profilen var ej developer, inget ska hända
			else:
				configEditor.add_section(profile)
				configEditor.set(profile, "ip", config[profile]["ip"])
				configEditor.set(profile, "port", config[profile]["port"])
				configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
				configEditor.set(profile, "username", config[profile]["username"])
				try:
					if config[profile]["developer_mode"]:
						configEditor.set(profile, "developer_mode", "True")
				except KeyError as e:
					pass #profilen var ej developer, inget ska hända

		with open('profiles.ini', 'w') as new_configfile:
			configEditor.write(new_configfile)
			config.read("profiles.ini") #detta fungerar inte, ingen aning om varför, kan inte hitta en lösning

	elif client_message == "/view -all":
		print("Profile name" + spacer(15, "Profile name") +
			  "IP addres" + spacer(13, "IP addres") +
			  "Port" + spacer(8, "port") +
			  "Network Protocol  " +
			  "Username")
		for profile in config.sections():
			print(profile +
				  (15 - len(profile)) * " " +
				  config[profile]["ip"] +
				  (13 - len(config[profile]["ip"])) * " " +
				  config[profile]["port"] +
				  (8 - len(config[profile]["port"])) * " " +
				  config[profile]["network_protocol"] +
				  (18 - len(config[profile]["network_protocol"])) * " " +
				  config[profile]["username"])

	elif client_message == "/view":
		print("Profile name" + spacer(15, "Profile name") +
			  "IP addres" + spacer(13, "IP addres") +
			  "Username")
		for profile in config.sections():
			print(profile +
				  (15 - len(profile)) * " " +
				  config[profile]["ip"] +
				  (13 - len(config[profile]["ip"])) * " " +
				  config[profile]["username"])

	else:
		s.send(str.encode(client_message)) #kommandot hittades inte utan skickas till servern
		pass # så att man enkelt ska kunna "döja" hela denna kod del i pycharm

def send_messages(): #the function that sends messages
	while True:
		client_message = input(">>>")
		if client_message[0:1] == "/":
			if command_interpreter(client_message): #lauches command intepreter
				s.close()
				os._exit(0)
		else:
			s.send(str.encode(client_message)) #was not a command

def recieve_messages(): #the function that recieves messages
	try:
		while True:
			server_message = s.recv(2048).decode('utf-8')
			if not server_message:
				raise ConnectionError #meddelandet är tomt, linux har lite svårt att fatta när det är dags att gå hem annars
			print (server_message)
	except ConnectionError as e: #this will happen when the server is shut down
		print("Disconnected from:", chat_server)

chat_server="127.0.0.1"
port=5555
username=""
developer_mode=0
config = configparser.ConfigParser()
config.read("profiles.ini")
network_protocol=""

command_dict={"/help":spacer(20, "/help") + "view this page",
			  "/quit":spacer(20, "/quit") + "exit program",
			  "/save [name]":spacer(20, "/save [name]") + "save profile settings as [name]",
			  "/del [name]":spacer(20, "/del [name]") + "delete profile [name]",
			  "/view":spacer(20, "/view") + "views your saved profiles",
			  "/edit [name]":spacer(20, "/edit [name]") + "edit profile [name]",
			  "/edit -all [name]":spacer(20, "/edit -all [name]") + "edit all avalible information about profile [name]",
			  "/view -all":spacer(20, "/view -all") + "views all inofmation avalible about you profiles"}

root_command_dict={"/terminate":spacer(20, "/terminate") + "terminates the server",
				   "/kick [username]":spacer(20, "/kick [username]") + "kicks [username] from the server"}

print("Select a proile to use or select manual:")
print("* manual")
for n in config.sections():
	print("*", n)

profile = input(">>>")
if profile in config.sections():
	network_protocol = str(config[profile]["network_protocol"])
	if network_protocol=="IPv4":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	elif network_protocol=="IPv6":
		s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
	else:
		print("Corrupt profile")
		os._exit(1)

	try:
		port = config.getint(profile, "port")
	except ValueError:
		print("Corrupt profile")
		os._exit(1)

	chat_server = config.get(profile, "ip")
	username = config.get(profile, "username")
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

sender = threading.Thread(target=send_messages, daemon=0)
reciever = threading.Thread(target=recieve_messages, daemon=0)
sender.start()
reciever.start()

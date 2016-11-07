import socket
import random
import threading
import os
import time
import configparser
import unicurses
from sys import platform


class CommmonMessageHoster:
    common_message=""

def getRaddr(conn):
    raw = str(conn)
    raddr = ""
    try:
        network_protocol = raw[raw.index("AF_INET"):raw.index("AF_INET") + len("AF_INET") + 1]
        if network_protocol == "AF_INET6":
            raddr = raw[raw.index("raddr=") + len("raddr="):len(raw) - 1]
            raddr = raddr.replace(", 0, 0)", "")
            raddr = raddr.replace("', ", ":")
            raddr = raddr[2:]
        elif (network_protocol == "AF_INET,"):
            raddr = raw[raw.index("raddr=") + len("raddr="):len(raw) - 1]
            raddr= raddr[1:-1]
            raddr=raddr.replace("'", "")
    except:
        print("[Error] Cannot identify raddr")
        raddr="[Error] Cannot identify raddr"
    return raddr

def listenToClient(conn, username):
	global taken_usernames, help, root_help
	raddr=""
	try:
		raddr=getRaddr(conn)
	except:
		raddr = getRaddr(conn)
	cmh.common_message = username + " connected"
	thread_manager.acquire()
	thread_manager.notify_all()
	thread_manager.release()
	while True:
		try:
			cmh.common_message = username + ":" + (conn.recv(2048)).decode("utf-8")
			print(cmh.common_message)
			if cmh.common_message.startswith(username+":/"): #commands
				if username=="root":
					if cmh.common_message=="root:/terminate":
						print("Terminating server")
						s.close()
						os._exit(0)
					elif cmh.common_message=="root:/users":
						cmh.common_message=cmh.common_message+"\nCurrently connected users:"
						for u in taken_usernames:
							cmh.common_message=cmh.common_message+"\n"+u
					elif cmh.common_message=="root:/enumerate":
						conn.send(str.encode("Number of live threads: "+str(threading.active_count())))
						for t in threading.enumerate():
							conn.send(str.encode(str(t)+"\n"))
						cmh.common_message=""
					elif cmh.common_message.startswith("root:/kick "):
#						if cmh.common_message[11:] in taken_usernames:
#							if taken_usernames[cmh.common_message[11:]]:
#								taken_usernames[cmh.common_message[11:]]=False
#							elif not taken_usernames[cmh.common_message[11:]]:
#								conn.send(str.encode("That user is not connected"))
						if cmh.common_message[11:] not in taken_usernames:
							conn.send(str.encode("That user is not connected"))
				if cmh.common_message.startswith(username+":/help"):
					if username == "root":
						conn.send(str.encode(help+root_help))
					else:
						conn.send(str.encode(help))
					cmh.common_message=""
				elif cmh.common_message.startswith(username+":/me"):
					cmh.common_message=username+cmh.common_message[len(username+":/me"):]
			thread_manager.acquire() #hämtar managern
			thread_manager.notify_all()  #notifera en random tråd som vändtar, kräver att managern är i tråden
			thread_manager.release()  # detta gör att manangern kan gå till andra trådar
		except ConnectionResetError:
			cmh.common_message= str(username) + " disconnected"
			thread_manager.acquire()
			thread_manager.notify_all()
			thread_manager.release()
			break
		except ConnectionAbortedError:
			cmh.common_message= str(username) + " was kicked"
			thread_manager.acquire()
			thread_manager.notify_all()
			thread_manager.release()
			break

def sendToClient(conn, listener, username):
	global taken_usernames
	while listener.is_alive():
		thread_manager.acquire() #hämtar managern
		thread_manager.wait() #säger till managern att "jag väntar på att någon ska notifiera mig"
							  #automatiskt: thread_manager.release() #se rad 3 under
							  # när den har blivt notifierad så hämtar den managern
#        thread_manager.notify() #notifera en random tråd som vändtar, kräver att managern är i tråden
							  # detta sker även här för att notify ska sprida sig till alla
		thread_manager.release() #detta gör att manangern kan gå till andra trådar
		if cmh.common_message == ("root:/kick "+username):
			conn.send(str.encode("You were kicked out <3"))
#			taken_usernames[username]=False
			taken_usernames.remove(username)
			conn.close()
			break
		else:
			try:
				conn.sendall(str.encode(cmh.common_message))
				time.sleep(0.01) #för att hindra den från att notifiera sig själv
			except ConnectionResetError:
				pass

def clientHandler(sock):
	global taken_usernames
	random_welcome_message = ["You want the crucible? I am the crucible.",
                              "FIGHT ON GERUDIAN!!!", "I can't believe what I'm seeing!",
                              "You can fight by my side anytime, Gaurdian",
                              "Is english class canceld tomorrow?"]
	sock.send(str.encode(random_welcome_message[random.randint(0, (len(random_welcome_message) - 1))]))
	username = (sock.recv(2048)).decode("utf-8")
	raddr = getRaddr(sock)
	
	if username in taken_usernames:
		sock.send(str.encode("That username is already taken."))
		print("Disconnected from "+raddr)
		sock.close()
		return
	elif username not in taken_usernames:
		taken_usernames.update([username])
	else:
		print("shit got weird")
		sock.send(str.encode("Something is wrong. Please report this event, and what you did to make this happen, to the server developer"))
		print("Disconnected from " + raddr)
		sock.close()
		return

	listener= threading.Thread(target=listenToClient,
                              daemon=1,
                              kwargs={'conn':sock, 'username':username},
                              name="L-" + username)
	sender = threading.Thread(target=sendToClient,
							  daemon=1,
                              kwargs={'conn':sock, 'listener':listener, 'username':username},
                              name="S-" + username)
	listener.start()
	sender.start()
	
	while listener.is_alive():
		time.sleep(0.1)
	if username in taken_usernames:
		taken_usernames.remove(username)
	print("Disconnected from " + raddr)

if platform == "win32":
	os.system("mode con: cols=90 lines=30")
config = configparser.ConfigParser()
config.read("config_server.ini")
print ('Enter "new" to create a new configuration profile, or select a pre-existing profile:\n'+str(config.sections()))
profile = input(">>>")
if str.lower(profile) == "new":
	profile = input("Profile name: ")
	while profile in config.sections():
		print("That profile name is already taken!")
		profile = input("Profile name: ")
	config[profile] = {}
	network_protocol = input("Network protocol (IPv4/IPv6): ")
	while (str.lower(network_protocol) != "ipv4") and (str.lower(network_protocol) != "ipv6"):
		print("Invalid protocol, it has to be IPv4 or IPv6!")
		network_protocol = str(input("Network protocol (IPv4/IPv6): "))
	config[profile]["network_protocol"] = network_protocol
	port = input("Port: ")
	while not str.isdigit(port):
		print("invalid port, try again.")
		port = input("port: ")
	port = int(port)
	config[profile]["port"] = str(port)
	max_population = input("Max population: ")
	while not str.isdigit(max_population):
		print("you should only enter numbers here")
		max_population = input("Max population: ")
	max_population = int(max_population)
	config[profile]["max_population"] = str(max_population)
	config.write(open("config_server.ini","w"))
elif profile in config.sections():
	network_protocol= str(config[profile]["network_protocol"])
	port = int(config[profile]["port"])
	max_population= int(config[profile]["max_population"])
else:
	print("invalid profile selected, default profile has been selected automatically")
	profile = "default"
	network_protocol= str(config[profile]["network_protocol"])
	port = int(config[profile]["port"])
	max_population= int(config[profile]["max_population"])
host = '0.0.0.0'
serverIP="placeholder4serverIP"
client_handlers=[]
cmh = CommmonMessageHoster()
lock = threading.Lock()
thread_manager = threading.Condition(lock) #tänk att detta är en manager som trådarna måste ha närvanade när det gör saker
s = socket
taken_usernames=set()
help=""
root_help="ROOT COMMANDS:"
command_dict={"/help":"View this message.",
			  "/me":"Works like the irc command"}
root_command_dict={"/users":"Returns a list of all connected users",
				   "/kick [username]":"Kicks the specified user.",
				   "/terminate":"Terminates the server",
				   "/enumerate":"Returns a list of all live threads"}

for command in command_dict:
	help+=command+" "*(20-len(command))+command_dict[command]+"\n"
for command in root_command_dict:
	root_help+="\n"+command+" "*(20-len(command))+root_command_dict[command]

if str.lower(network_protocol)=="ipv6":
	s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
elif str.lower(network_protocol)=="ipv4":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    print("Invalid network protocol")
    os._exit(1)

try:
    s.bind((host, port))
except socket.error as e:
    print("Failed to bind\n", e)
    os._exit(1)

s.listen()
print("Using "+network_protocol)
print("Max population:",max_population)
print("Listening @ ",serverIP + ":" + str(port))

while 1:
	for n in range(len(client_handlers)):
		if not client_handlers[n].is_alive():
			client_handlers.pop(n)
			break

	sock, address = s.accept()
	if len(client_handlers) > max_population:
		sock.send(str.encode("Server full, try again later"))
		sock.close()
		continue #skippar resten av loopen och börjar om från början
	print('connected to ' + address[0] + ':' + str(address[1]))
	client_handlers.append(threading.Thread(kwargs={'sock':sock}, #passar sock som argument. kwargs=keyword arguments
                                            target=clientHandler, # när den startar kommer den att starta med clientHandler
                                            daemon=1))            # när programmet avslutas så dör även threaden (kanske löser linux upptagna portar?)
	client_handlers[len(client_handlers)-1].start()               # startar threaden
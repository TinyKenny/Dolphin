#import socket
import random
import threading
import os
import time
import configparser
import unicurses
import socketserver
from sys import platform
"""
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
    raddr=""
    try:
        raddr=getRaddr(conn)
    except:
        raddr = getRaddr(conn)
    while 1:
        try:
            cmh.common_message = username + ":" + (conn.recv(2048)).decode("utf-8")
            print(cmh.common_message)
            thread_manager.acquire() #hämtar managern
            thread_manager.notify()  #notifera en random tråd som vändtar, kräver att managern är i tråden
            thread_manager.release()  # detta gör att manangern kan gå till andra trådar
            if cmh.common_message=="root:terminate":
                print("Terminating server")
                s.close()
                os._exit(0)
        except ConnectionResetError:
            cmh.common_message= str(username) + " disconnected"
            break

def sendToClient(conn):
    while 1:
        thread_manager.acquire() #hämtar managern
        thread_manager.wait() #säger till managern att "jag väntar på att någon ska notifiera mig"
                              #automatiskt: thread_manager.release() #se rad 3 under
                              # när den har blivt notifierad så hämtar den managern
        thread_manager.notify() #notifera en random tråd som vändtar, kräver att managern är i tråden
                                # detta sker även här för att notify ska sprida sig till alla
        thread_manager.release() #detta gör att manangern kan gå till andra trådar
        try:
            conn.sendall(str.encode(cmh.common_message))
            time.sleep(0.01) #för att hindra den från att notifiera sig själv
        except ConnectionResetError:
            pass

def clientHandler(sock):
    random_welcome_message = ["You want the crucible? I am the crucible.",
                              "FIGHT ON GERUDIAN!!!", "I can't believe what I'm seeing!",
                              "You can fight by my side anytime, Gaurdian",
                              "Is english class canceld tomorrow?"]
    sock.send(str.encode(random_welcome_message[random.randint(0, (len(random_welcome_message) - 1))]))
    username = (sock.recv(2048)).decode("utf-8")
    raddr = getRaddr(sock)
    sender = threading.Thread(target=sendToClient,
                              daemon=1,
                              kwargs={'conn':sock},
                              name="S" + raddr)
    listner= threading.Thread(target=listenToClient,
                              daemon=1,
                              kwargs={'conn':sock, 'username':username},
                              name="L" + raddr)
    sender.start()
    listner.start()

    while listner.is_alive():
        time.sleep(0.1)
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
	while str.lower(network_protocol) != ("ipv4" and "ipv6"):
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
host = ''
serverIP="placeholder4serverIP"
client_handlers=[]
cmh = CommmonMessageHoster()
lock = threading.Lock()
thread_manager = threading.Condition(lock) #tänk att detta är en manager som trådarna måste ha närvanade när det gör saker
s = socket


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

    client_handlers.append(threading.Thread(kwargs={'sock':sock}, #passar sock som argument. kwargs=keyword arguments
                                            target=clientHandler, # när den startar kommer den att starta med clientHandler
                                            daemon=1))            # när programmet avslutas så dör även threaden (kanske löser linux upptagna portar?)
    client_handlers[len(client_handlers)-1].start()               # startar threaden
    print('connected to ' + address[0] + ':' + str(address[1]))
"""
#test-area starts here
"""
host="0.0.0.0"
port=5555
s=socketserver.TCPServer((host,port),False)

class SomeHandler(socketserver.BaseRequestHandler):
	def handle(self):
		self.data=self.request.recv(2048).strip()
		self.request.sendall(self.data.upper())
"""

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
#        self.reply = ("{} wrote:".format(self.client_address[0])+"\n"+self.data)
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data)

if __name__ == "__main__":
    HOST, PORT = "localhost", 5555

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()






































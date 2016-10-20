import socket
import random
from _thread import *

class ClientHandler:
    common_message=""

    def listenToClient(self, conn, username):
        raw = str(conn)
        raddr=""
        network_protocol = raw[raw.index("AF_INET"):raw.index("AF_INET") + len("AF_INET") + 1]

        if network_protocol=="AF_INET6":
            raddr = raw[raw.index("raddr=")+len("raddr="):len(raw)-1]
        elif(network_protocol=="AF_INET,"):
            raddr = raw[raw.index("raddr=") + len("raddr="):len(raw) - 1]
        else:
            print("[Error] Cannot identify networkprotocol")
            exit()

        while 1:
            try:
                self.common_message = username + ":" + (conn.recv(2048)).decode("utf-8")
                print(self.common_message)
            except ConnectionResetError:
                self.common_message= str(username) + " disconnected"
                print("Disconnected from "+raddr)
                break

    def sendToClient(self, conn):
        last_common_message = ""
        while 1:
            if self.common_message != last_common_message:
                try:
                    conn.sendall(str.encode(self.common_message))
                    last_common_message = self.common_message
                except ConnectionResetError:
                    break

    def clientHandler(self, sock):
        shaxx_quote = ["You want the crucible? I am the crucible.",
                       "FIGHT ON GERUDIAN!!!", "I can't believe what I'm seeing!",
                       "You can fight by my side anytime, Gaurdian",
                       "Is english class canceld tomorrow?"]
        sock.send(str.encode(shaxx_quote[random.randint(0, (len(shaxx_quote) - 1))]))
        username = (conn.recv(2048)).decode("utf-8")
        start_new_thread(self.sendToClient, (self, sock,))
        start_new_thread(self.listenToClient, (self, sock, username, ))

host = ''
port = 5555
max_population=5
client_handlers=[]
common_message=""
network_protocol= "IPv6"

s = socket
if network_protocol=="IPv6":
    s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
elif network_protocol=="IPv4":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
else:
    print("Invalid network protocol")
    exit()

try:
    s.bind((host, port))
except socket.error as e:
    print(e)

s.listen(max_population)
print("Listening @ port",port)
print("Max population:",max_population)

while 1:
    conn, addr = s.accept()
    client_handlers.append(ClientHandler)
    print('Connected to ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(client_handlers[len(client_handlers)-1].clientHandler, (ClientHandler, conn, ))



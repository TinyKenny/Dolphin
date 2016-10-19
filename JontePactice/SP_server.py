import socket
import sys
from _thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 5555

try:
    s.bind((host, port))
except socket.error as e:
    print(e)

s.listen(5)
print("Waiting for connection")

def threaded_client_handler(conn, IPv4, port):
    conn.send(str.encode("Hello World!"))
    while 1:

        try:
            data = conn.recv(2048)
            if not data:
                break
            reply = 'client says: ' + data.decode('utf-8')
            #conn.sendall(str.encode(reply))
        except socket.error as e:
            print(e)
            break
    print("closed connection to"+IPv4+":"+port)
    conn.close()

while 1:
    conn, addr = s.accept()
    print('connected to ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client_handler, (conn,  addr[0], str(addr[1])))
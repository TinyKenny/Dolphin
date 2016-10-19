import socket
import sys
import random
from _thread import *

shaxx_quote=["You want the crucible? I am the crucible.", "FIGHT ON GERUDIAN!!!", "I can't believe what I'm seeing!", "You can fight by my side anytime, Gaurdian"]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = ''
port = 5555

try:
    s.bind((host, port))
except socket.error as e:
    print(e)

s.listen(5)
print("Waiting for connection")

def threaded_client_handler(conn):
    conn.send(str.encode(shaxx_quote[random.randint(0, (len(shaxx_quote)-1))]))
    print("yes this is the client speaking")
    while 1:
        data = conn.recv(2048)
        reply = 'Server output: ' + data.decode('utf-8')
        if not data:
            break
        conn.sendall(str.encode(reply))
    conn.close()

while 1:
    conn, addr = s.accept()
    print('connected to ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(threaded_client_handler, (conn, ))
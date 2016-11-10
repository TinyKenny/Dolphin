import threading
import time
import socket
import os
import sys
from unicurses import *



def chatlog(high, wide, sender):
	global server_welcome_message
	global chat_server
	my_output = [0]*2
	my_out_pans = [0]*2
	my_output[0] = newwin(high-3,wide,0,0)
	my_output[1] = newwin(high-5,wide-2,1,1)
	box(my_output[0],0,0)
	scrollok(my_output[1],1)
	my_out_pans[0] = new_panel(my_output[0])
	my_out_pans[1] = new_panel(my_output[1])
	waddstr(my_output[1],"Connected to: "+str(chat_server)+"\n"+server_welcome_message)
	update_panels()
	doupdate()
	while sender.is_alive():
		try:
			server_message=s.recv(2048).decode('utf-8')
			waddstr(my_output[1],"\n"+server_message)
			update_panels()
			doupdate()
		except:
			waddstr(my_output[1],"oh shiiiit")
			os._exit(1)
	s.close()
	os.exit

def send_messages(high, wide):
	my_input = [0]*2
	my_in_pans = [0]*2
	my_input[0]=newwin(3,wide,high-3,0)
	my_input[1]=newwin(1,wide-5,high-2,4)
	box(my_input[0],0,0)
	my_in_pans[0]=new_panel(my_input[0])
	my_in_pans[1]=new_panel(my_input[1])
	mvwaddstr(my_input[0],1,1,">>>")
	update_panels()
	doupdate()
	while True:
		client_message=wgetstr(my_input[1])
		if client_message == "/quit":
			break
		s.send(str.encode(client_message))
		werase(my_input[1])
		update_panels()
		doupdate()
#funct end

address_protocol="ipv4"
chat_server="localhost"
port=5555
username="root"

stdscr = initscr()
clear()
cbreak()
echo()
HEIGHT,WIDTH = getmaxyx(stdscr)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
	s.connect((chat_server,port))
	server_welcome_message=s.recv(2048).decode('utf-8')
	s.send(str.encode(username))
except socket.error as e:
	print(e)
	os._exit(1)




sender = threading.Thread(target=send_messages,daemon=False,kwargs={"high":HEIGHT,"wide":WIDTH})
reciever = threading.Thread(target=chatlog,daemon=False,kwargs={"high":HEIGHT,"wide":WIDTH,"sender":sender})
sender.start()
reciever.start()
sender.join()
reciever.join()
endwin()
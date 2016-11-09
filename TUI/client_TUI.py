import threading
import socket
import os
from unicurses import *

def chatlog(high, wide, sender):
	my_output = [0]*(high-4)
	my_out_pans = [0]*(high-4)
	my_log = [""]*(high-5)
	my_output[0]=newwin(high-3,wide,0,0)
	box(my_output[0],0,0)
	for i in range(1,(high-4)):
		my_output[i]=newwin(1,wide-2,high-4-i,1)
	for i in range(0,(high-4)):
		my_out_pans[i]=new_panel(my_output[i])
	update_panels()
	doupdate()
	while sender.is_alive():
		try:
			for i in range(2,(high-4)):
				my_log[high-4-i] = my_log[high-5-i]
			message_data=s.recv(2048)
			my_log[0]=message_data.decode('utf-8')
			for i in range(1,(high-5)):
				werase(my_output[i])
			for i in range(1,(high-5)):
				waddstr(my_output[i],my_log[i-1])
			update_panels()
			doupdate()
		except:
			waddstr(my_output[1],"oh shiiiit")
			os._exit(1)

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
	data=s.recv(2048)
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

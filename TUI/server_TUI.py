import socket
import random
import threading
import os
import time
import configparser
from unicurses import *
from sys import platform


class CommmonMessageHoster:
    common_message=""

def getRaddr(conn):
    global logwin
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
        waddstr(logwin,"[Error] Cannot identify raddr")
        wrefresh(logwin)
        raddr="[Error] Cannot identify raddr"
    return raddr

def listenToClient(conn, username):
	global taken_usernames, help, root_help, root_pass, logwin
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
			waddstr(logwin, "\n"+cmh.common_message)
			wrefresh(logwin)
			if cmh.common_message.startswith(username+":/"): #commands
				if taken_usernames[username]:
					if cmh.common_message==username+":/terminate":
						waddstr(logwin,"\nTerminating server")
						wrefresh(logwin)
						s.close()
						endwin()
						os._exit(0)
					elif cmh.common_message==username+":/users -show":
						cmh.common_message=cmh.common_message+"\nCurrently connected users:"
						for u in taken_usernames:
							cmh.common_message=cmh.common_message+"\n"+u
					elif cmh.common_message==(username+":/users"):
						conn.send(str.encode("not implemented yet, use '/users -show' instead"))
					elif cmh.common_message=="root:/enumerate":
						conn.send(str.encode("Number of live threads: "+str(threading.active_count())))
						for t in threading.enumerate():
							conn.send(str.encode(str(t)+"\n"))
						cmh.common_message=""
					elif cmh.common_message.startswith(username+":/kick "):
						if cmh.common_message[len(username)+7:] not in taken_usernames:
							conn.send(str.encode("That user is not connected"))
				elif cmh.common_message==username+":/root "+root_pass and not taken_usernames[username]:
					taken_usernames[username]=True
					conn.send(str.encode("You now have admin rights!"))
					cmh.common_message=""
				if cmh.common_message.startswith(username+":/help"):
					if taken_usernames[username]:
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
		except BrokenPipeError:
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
	global taken_usernames, logwin
	while listener.is_alive():
		thread_manager.acquire() #hämtar managern
		thread_manager.wait() #säger till managern att "jag väntar på att någon ska notifiera mig"
							  #automatiskt: thread_manager.release() #se rad 3 under
							  # när den har blivt notifierad så hämtar den managern
#        thread_manager.notify() #notifera en random tråd som vändtar, kräver att managern är i tråden
							  # detta sker även här för att notify ska sprida sig till alla
		thread_manager.release() #detta gör att manangern kan gå till andra trådar
		if cmh.common_message.endswith(":/kick "+username) and taken_usernames[cmh.common_message.rsplit(":")[0]]:
			conn.send(str.encode("You were kicked out <3"))
			del taken_usernames[username]
			conn.close()
			break
		else:
			try:
				conn.sendall(str.encode(cmh.common_message))
				time.sleep(0.01) #för att hindra den från att notifiera sig själv
			except ConnectionResetError:
				pass

def clientHandler(sock):
	global taken_usernames, logwin
	random_welcome_message = ["You want the crucible? I am the crucible.",
                              "FIGHT ON GERUDIAN!!!",
							  "I can't believe what I'm seeing!",
                              "You can fight by my side anytime, Gaurdian",
                              "Is english class canceld tomorrow?"]
	sock.send(str.encode(random_welcome_message[random.randint(0, (len(random_welcome_message) - 1))]))
	username = (sock.recv(2048)).decode("utf-8")
	raddr = getRaddr(sock)
	
	if username in taken_usernames:
		sock.send(str.encode("That username is already taken."))
		waddstr(logwin,"\nDisconnected from "+raddr)
		wrefresh(logwin)
		sock.close()
		return
	elif username not in taken_usernames:
		taken_usernames[username]=False
	else:
		waddstr(logwin,"\nSomething went wrong with the username check.")
		sock.send(str.encode("Something is wrong. Please report this event, and what you did to make this happen, to the server developer"))
		waddstr(logwin,"\nDisconnected from " + raddr)
		wrefresh(logwin)
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
		del taken_usernames[username]
	waddstr(logwin,"\nDisconnected from " + raddr)
	wrefresh(logwin)

def print_menu(prof_select_win, highlight):
	x = 2
	y = 2
	box(prof_select_win, 0, 0)
	for i in range(0, n_choices):
		if (highlight == i + 1):
			wattron(prof_select_win, A_REVERSE)
			mvwaddstr(prof_select_win, y, x, choices[i])
			wattroff(prof_select_win, A_REVERSE)
		else:
			mvwaddstr(prof_select_win, y, x, choices[i])
		y += 1
	wrefresh(prof_select_win)

def destroy_win(local_win):
	wborder(local_win, CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '))
	wclear(local_win)
	wrefresh(local_win)
	delwin(local_win)


if platform == "win32":
	os.system("mode con: cols=90 lines=30")	

WIDTH = 30
HEIGHT = 10
config = configparser.ConfigParser()
config.read("config_server.ini")
choices = config.sections()
choices.append("New")
n_choices = len(choices)
highlight = 1
profile = 0
c = 0

stdscr = initscr()
clear()
noecho()
cbreak()
curs_set(0)
startx = int((90 - WIDTH) / 2)
starty = int((30 - HEIGHT) / 2)

prof_select_win = newwin(HEIGHT, WIDTH, starty, startx)
keypad(prof_select_win, True)
mvaddstr(0, 0, "Select a pre-existing configuration profile, or create a new profile")
mvaddstr(1, 0, "Use arrow keys navigate, press enter to select")
refresh()
print_menu(prof_select_win, highlight)

while True:
	c = wgetch(prof_select_win)
	if c == KEY_UP:
		if highlight == 1:
			highlight == n_choices
		else:
			highlight -= 1
	elif c == KEY_DOWN:
		if highlight == n_choices:
			highlight = 1
		else:
			highlight += 1
	elif c == 10:   # ENTER is pressed
		profile = choices[highlight-1]
		clrtoeol()
		refresh()
		break
	else:
		mvaddstr(29, 0, str.format("Character pressed is = {0}", c))
		clrtoeol()
		refresh()
	print_menu(prof_select_win, highlight)
destroy_win(prof_select_win)
clear()
echo()
curs_set(1)
refresh()
if profile == "New":
	new_prof_box=newwin(20,60,int(5),15)
	new_prof_win=newwin(18,58,6,16)
	box(new_prof_box,0,0)
	wrefresh(new_prof_box)
	mvwaddstr(new_prof_win,0,0,"Profile name: ")
	wrefresh(new_prof_win)
	profile=wgetstr(new_prof_win)
	while profile in config.sections() or profile.lower() == "new" or profile == "":
		mvaddstr(29,0,"Profile name already taken.")
		mvwaddstr(new_prof_win,0,0,"Profile name: ")
		wclrtoeol(new_prof_win)
		refresh()
		profile=wgetstr(new_prof_win)
	#config[profile]={}
	mvaddstr(29,0," ")
	clrtoeol()
	mvwaddstr(new_prof_win,1,0,"Network protocol: ")
	refresh()
	network_protocol=wgetstr(new_prof_win)
	while network_protocol.lower() != "ipv4":
		mvaddstr(29,0,"Only IPv4 is supported at the moment.")
		mvwaddstr(new_prof_win,1,0,"Network protocol: ")
		wclrtoeol(new_prof_win)
		refresh()
		network_protocol=wgetstr(new_prof_win)
	#config[profile]["network_protocol"]=network_protocol
	mvaddstr(29,0," ")
	clrtoeol()
	mvwaddstr(new_prof_win,2,0,"Port: ")
	refresh()
	port=wgetstr(new_prof_win)
	while port == ""  or not str.isdigit(port):
		mvaddstr(29,0,"Invalid port, please try again.")
		mvwaddstr(new_prof_win,2,0,"Port: ")
		wclrtoeol(new_prof_win)
		refresh()
		port=wgetstr(new_prof_win)
	#config[profile]["port"]=port
	port=int(port)
	mvaddstr(29,0," ")
	clrtoeol()
	mvwaddstr(new_prof_win,3,0,"Max population: ")
	refresh()
	max_population=wgetstr(new_prof_win)
	while max_population == "" or not str.isdigit(max_population):
		mvaddstr(29,0,"You should only enter numbers here.")
		mvwaddstr(new_prof_win,3,0,"Max population: ")
		wclrtoeol(new_prof_win)
		refresh()
		max_population=wgetstr(new_prof_win)
	#config[profile]["max_population"]=max_population
	max_population=int(max_population)
	mvaddstr(29,0," ")
	clrtoeol()
	mvwaddstr(new_prof_win,4,0,"Root password: ")
	refresh()
	root_pass=wgetstr(new_prof_win)
	while root_pass == "":
		mvaddstr(29,0,"You can't just leave this blank!")
		mvwaddstr(new_prof_win,4,0,"Root password: ")
		wclrtoeol(new_prof_win)
		refresh()
		root_pass=wgetstr(new_prof_win)
	#config[profile]["root_pass"]=root_pass
	config.write(open("config_server.ini","w"))
	destroy_win(new_prof_box)
	destroy_win(new_prof_win)
	clear()
	refresh()
else:
	network_protocol=str(config[profile]["network_protocol"])
	port=int(config[profile]["port"])
	max_population=int(config[profile]["max_population"])
	root_pass=str(config[profile]["root_pass"])

host='0.0.0.0'
serverIP="placeholder4serverIP"
client_handlers=[]
cmh = CommmonMessageHoster()
lock = threading.Lock()
thread_manager = threading.Condition(lock) #tänk att detta är en manager som trådarna måste ha närvanade när det gör saker
taken_usernames=dict()
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

logbox=newwin(27,90,0,0)
logwin=newwin(24,88,1,1)
inpbox=newwin(3,90,27,0)
inpwin=newwin(1,88,28,1)
box(logbox,0,0)
box(inpbox,0,0)
scrollok(logwin,1)
wrefresh(logbox)
wrefresh(inpbox)
refresh()

try:
	s.bind((host,port))
except socket.error as e:
	waddstr(logwin,"Failed to bind\n"+e)
	wrefresh(logwin)
	getch()
	endwin()
	os._exit(1)

s.listen()
waddstr(logwin,"Using "+network_protocol+"\nMax population: "+str(max_population)+"\nListening @ "+serverIP+":"+str(port))
wrefresh(logwin)

while 1:
	for n in range(len(client_handlers)):
		if not client_handlers[n].is_alive():
			client_handlers.pop(n)
			break
	sock, address = s.accept()
	if len(client_handlers) > max_population:
		sock.send(str.encode("Server full, try again later"))
		sock.close()
		continue
	waddstr(logwin,"\nConnected to "+address[0]+":"+str(address[1]))
	wrefresh(logwin)
	client_handlers.append(threading.Thread(kwargs={'sock':sock},
											target=clientHandler,
											daemon=1))
	client_handlers[len(client_handlers)-1].start()

getch()
refresh()
endwin()

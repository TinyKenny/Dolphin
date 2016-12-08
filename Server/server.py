import random
import threading
import os
import time
import datetime
import configparser
import socketserver
from sys import platform
from unicurses import *

class CommonMessageHoster:
    common_message=""

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global taken_usernames, logwin
        random_welcome_message = ["You want the crucible? I am the crucible.",
                                  "FIGHT ON GERUDIAN!!!",
                                  "I can't believe what I'm seeing!",
                                  "You can fight by my side anytime, Gaurdian",
                                  "Is english class canceld tomorrow?",
                                  "Livet är inte optimalt.",
                                  "Show your support! Purchase Dolphin Pro - Premium edition today!",
                                  "Skolan måste vara tråkig, annars jobbar man inte."]
        self.request.send(str.encode(random_welcome_message[random.randint(0, (len(random_welcome_message) - 1))]))
        username = (self.request.recv(2048)).decode("utf-8")
        raddr = getRaddr(self.request)
        
        while username in taken_usernames or username.lower() == "server announcement" or username.lower() == "server announcement:":
            self.request.send(str.encode("That username is already taken. Please select a new one."))
            username = (self.request.recv(2048))
        taken_usernames[username] = False
        
        listener= threading.Thread(target=listenToClient,
                                  daemon=True,
                                  kwargs={'conn':self.request, 'username':username},
                                  name="L-" + username)
        sender = threading.Thread(target=sendToClient,
                                  daemon=True,
                                  kwargs={'conn':self.request, 'listener':listener, 'username':username},
                                  name="S-" + username)
        listener.start()
        sender.start()
        
        while listener.is_alive():
            time.sleep(0.1)
        if username in taken_usernames:
            del taken_usernames[username]
        waddstr(logwin,"\nDisconnected from " + raddr)
        wrefresh(logwin)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def destroy_win(local_win):
    wborder(local_win, CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '), CCHAR(' '))
    wclear(local_win)
    wrefresh(local_win)
    delwin(local_win)

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

def interpret_commands(conn, username):
    global taken_usernames, help, root_help, root_pass, logwin
    if taken_usernames[username]: #root commands
        if cmh.common_message[11:]==username+":/terminate":
            waddstr(logwin,"\n"+time.strftime("[%H:%M:%S] ")+"Terminating server.")
            with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                chatlog.write(time.strftime("[%H:%M:%S] ")+"Terminating server.\n")
            wrefresh(logwin)
            server.shutdown()
            server.close_server()
            return("")
        elif cmh.common_message[11:]==username+":/users -show":
            users=cmh.common_message+"\nCurrently connected users:"
            for u in taken_usernames:
                users=users+"\n"+u
            return(users)
        elif cmh.common_message[11:]==username+":/users":
            conn.send(str.encode(str(taken_usernames)))
            return("")
        elif cmh.common_message[11:].startswith(username+":/kick "):
            if cmh.common_message[11+len(username+":/kick "):] not in taken_usernames:
                conn.send(str.encode(cmh.common_message+"\nThat user is not connected."))
                return("")
            elif taken_usernames[cmh.common_message[11+len(username+":/kick "):]]:
                conn.send(str.encode(cmh.common_message+"\nYou can't kick that user."))
                return("")
    elif cmh.common_message[11:]==username+":/root "+root_pass:
        taken_usernames[username]=True
        conn.send(str.encode("You have admin rights!"))
        return("")
    if cmh.common_message[11:]==username+":/help":
        if taken_usernames[username]:
            conn.send(str.encode(help+root_help))
            return("")
        else:
            conn.send(str.encode(help))
            return("")
    elif cmh.common_message[11:].startswith(username+":/me"):
        return (time.strftime("[%H:%M:%S] ")+username+cmh.common_message[11+len(username+":/me"):])
    return(cmh.common_message)

def listenToClient(conn, username):
    global taken_usernames, help, root_help, root_pass, logwin
    raddr=""
    try:
        raddr=getRaddr(conn)
    except:
        raddr = getRaddr(conn)
    cmh.common_message = time.strftime("[%H:%M:%S] ")+ username + " connected"
    thread_manager.acquire()
    thread_manager.notify_all()
    thread_manager.release()
    while True:
        try:
            message_data=(conn.recv(2048)).decode("utf-8")
            if message_data == "":
                break
            cmh.common_message = time.strftime("[%H:%M:%S] ") + username + ":" + message_data
            waddstr(logwin, "\n"+cmh.common_message)
            wrefresh(logwin)
            if cmh.common_message[11:].startswith(username+":/"): #commands
                cmh.common_message = interpret_commands(conn, username)
            with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                chatlog.write(cmh.common_message+"\n")
            thread_manager.acquire() #hämtar managern
            thread_manager.notify_all()  #notifera en random tråd som vändtar, kräver att managern är i tråden
            thread_manager.release()  # detta gör att manangern kan gå till andra trådar
        except ConnectionResetError:
            cmh.common_message= time.strftime("[%H:%M:%S] ") + str(username) + " disconnected"
            with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                chatlog.write(cmh.common_message+"\n")
            thread_manager.acquire()
            thread_manager.notify_all()
            thread_manager.release()
            break
        except BrokenPipeError:
            cmh.common_message= time.strftime("[%H:%M:%S] ") + str(username) + " disconnected"
            with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                chatlog.write(cmh.common_message+"\n")
            thread_manager.acquire()
            thread_manager.notify_all()
            thread_manager.release()
            break
        except ConnectionAbortedError:
            cmh.common_message= time.strftime("[%H:%M:%S] ") + str(username) + " was kicked"
            with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                chatlog.write(cmh.common_message+"\n")
            thread_manager.acquire()
            thread_manager.notify_all()
            thread_manager.release()
            break

def make_new_profile(config):
    new_prof_box=newwin(20,60,int(5),15)
    new_prof_win=newwin(18,58,6,16)
    box(new_prof_box,0,0)
    wrefresh(new_prof_box)
    while True: #Profile name
        mvwaddstr(new_prof_win,0,0,"Profile name: ")
        wclrtoeol(new_prof_win)
        refresh()
        profile=wgetstr(new_prof_win)
        if profile not in config.sections() and profile.lower() != "new" and profile != "":
            break
        mvaddstr(29,0,"Profile name already taken.")
    config[profile]={}
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Port select
        mvwaddstr(new_prof_win,1,0,"Port: ")
        wclrtoeol(new_prof_win)
        refresh()
        port=wgetstr(new_prof_win)
        if port != "" and str.isdigit(port):
            break
        mvaddstr(29,0,"Invalid port, please try again.")
    config[profile]["port"]=port
    port=int(port)
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Max population
        mvwaddstr(new_prof_win,2,0,"Max population: ")
        wclrtoeol(new_prof_win)
        refresh()
        max_population=wgetstr(new_prof_win)
        if max_population != "" and str.isdigit(max_populaiton):
            break
        mvaddstr(29,0,"You should only enter numbers here.")
    config[profile]["max_population"]=max_population
    max_population=int(max_population)
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Root password
        mvwaddstr(new_prof_win,3,0,"Root password: ")
        wclrtoeol(new_prof_win)
        refresh()
        root_pass=wgetstr(new_prof_win)
        if root_pass != "":
            break
        mvaddstr(29,0,"You can't just leave this blank!")
    config[profile]["root_pass"]=root_pass
    config.write(open("config_server.ini","w"))
    destroy_win(new_prof_box)
    destroy_win(new_prof_win)
    clear()
    refresh()
    return(profile,port,max_population,root_pass)

def make_temp_profile():
    new_prof_box=newwin(20,60,int(5),15)
    new_prof_win=newwin(18,58,6,16)
    box(new_prof_box,0,0)
    wrefresh(new_prof_box)
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Port select
        mvwaddstr(new_prof_win,0,0,"Port: ")
        wclrtoeol(new_prof_win)
        refresh()
        port=wgetstr(new_prof_win)
        if port != "" and str.isdigit(port):
            break
        mvaddstr(29,0,"Invalid port, please try again.")
    port=int(port)
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Max population
        mvwaddstr(new_prof_win,1,0,"Max population: ")
        wclrtoeol(new_prof_win)
        refresh()
        max_population=wgetstr(new_prof_win)
        if max_population != "" and str.isdigit(max_population):
            break
        mvaddstr(29,0,"You should only enter numbers here.")
    max_population=int(max_population)
    mvaddstr(29,0," ")
    clrtoeol()
    refresh()
    while True: #Root password
        mvwaddstr(new_prof_win,2,0,"Root password: ")
        wclrtoeol(new_prof_win)
        refresh()
        root_pass=wgetstr(new_prof_win)
        if root_pass != "":
            break
        mvaddstr(29,0,"You can't just leave this blank!")
    destroy_win(new_prof_box)
    destroy_win(new_prof_win)
    clear()
    refresh()
    return (port,max_population,root_pass)

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

def sendToClient(conn, listener, username):
    global taken_usernames, logwin
    while listener.is_alive():
        thread_manager.acquire() #hämtar managern
        thread_manager.wait() #säger till managern att "jag väntar på att någon ska notifiera mig"
                              #automatiskt: thread_manager.release() #se rad 3 under
                              # när den har blivt notifierad så hämtar den managern
                              # detta sker även här för att notify ska sprida sig till alla
        thread_manager.release() #detta gör att manangern kan gå till andra trådar
        if cmh.common_message.endswith(":/kick "+username) and taken_usernames[cmh.common_message[11:].rsplit(":")[0]]:
            if random.randint(0,255) < 1:
                conn.send(str.endoce("Error: Dolphin Premium edition required"))
            else:
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
            except BrokenPipeError:
                pass

def server_input():
    global inpwin, logwin, taken_usernames
    username = "SERVER"
    while True:
        server_message = wgetstr(inpwin)
        werase(inpwin)
        wrefresh(inpwin)
        cmh.common_message=time.strftime("[%H:%M:%S] ")+username+":"+server_message
        waddstr(logwin,"\n"+cmh.common_message)
        wrefresh(logwin)
        if server_message.startswith("/"): #A lightweight, slightly modified verision of interpret_commands.
            if server_message == "/terminate":
                waddstr(logwin,"\n"+time.strftime("[%H:%M:%S] ")+"Terminating server.")
                with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
                    chatlog.write(time.strftime("[%H:%M:%S] ")+"Terminating server.\n")
                wrefresh(logwin)
                server.shutdown()
                server.server_close()
            elif server_message == "/users -show":
                users = "\nCurrently connected users:"
                for u in taken_usernames:
                    users=users+"\n"+u
                cmh.common_message=cmh.common_message+users
                waddstr(logwin,users)
                wrefresh(logwin)
            elif server_message == "/users":
                cmh.common_message=""
                waddstr(logwin,"\n"+str(taken_usernames))
                wrefresh(logwin)
            elif server_message.startswith("/kick "):
                if server_message[len("/kick "):] not in taken_usernames:
                    waddstr(logwin,"\nThat user is not connected.")
                    wrefresh(logwin)
            elif server_message == "/help":
                cmh.common_message=""
                waddstr(logwin,"\n"+help+root_help+server_help)
                wrefresh(logwin)
            elif server_message.startswith("/me"):
                cmh.common_message=time.strftime("[%H:%M:%S] ")+username+server_message[len("/me"):]
                waddstr(logwin,"\n"+cmh.common_message)
                wrefresh(logwin)
            elif server_message.startswith("/promote "):
                if server_message[len("/promote "):] not in taken_usernames:
                    waddstr(logwin,"\nThat user is not connected.")
                    wrefresh(logwin)
                    cmh.common_message=""
                elif taken_usernames[server_message[len("/promote "):]]:
                    waddstr(logwin,"\nThat user already has admin rights!")
                    wrefresh(logwin)
                    cmh.common_message=""
                else:
                    taken_usernames[server_message[len("/promote "):]]=True
                    waddstr(logwin,"\n"+time.strftime("[%H:%M:%S] ")+"Server Announcement: "+server_message[len("/promote "):]+" has been promoted.")
                    wrefresh(logwin)
                    cmh.common_message=time.strftime("[%H:%M:%S] ")+"Server Announcement: "+server_message[len("/promote "):]+" has been promoted."
            elif server_message.startswith("/demote "):
                if server_message[len("/demote "):] not in taken_usernames:
                    waddstr(logwin,"\nThat user is not connected.")
                    wrefresh(logwin)
                    cmh.common_message=""
                elif not taken_usernames[server_message[len("/demote "):]]:
                    waddstr(logwin,"\nThat user doesn't have admin rights!")
                    wrefresh(logwin)
                    cmh.common_message=""
                else:
                    taken_usernames[server_message[len("/demote "):]]=False
                    waddstr(logwin,"\n"+time.strftime("[%H:%M:%S] ")+"Server Announcement: "+server_message[len("/demote "):]+" has been demoted.")
                    wrefresh(logwin)
                    cmh.common_message=time.strftime("[%H:%M:%S] ")+"Server Announcement: "+server_message[len("/demote "):]+" has been demoted."
        with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
            chatlog.write(cmh.common_message+"\n")
        thread_manager.acquire()
        thread_manager.notify_all()
        thread_manager.release()




if not os.path.exists("./serverlogs"):
	os.makedirs("./serverlogs")
	os.makedirs("./serverlogs/debug")
	os.makedirs("./serverlogs/chatlogs")
else:
	if not os.path.exists("./serverlogs/debug"):
		os.makedirs("./serverlogs/debug")
	if not os.path.exists("./serverlogs/chatlogs"):
		os.makedirs("./serverlogs/chatlogs")
with open("./serverlogs/chatlogs/"+str(datetime.date.today())+".txt","a") as chatlog:
	chatlog.write("Server started.\n")

if platform == "win32":
	os.system("mode con: cols=90 lines=30")	
elif platform == "linux":
	os.system("set noglob; setenv COLUMNS '90'; setenv LINES '30'; unset noglob")

WIDTH = 30
HEIGHT = 10
config = configparser.ConfigParser()
config.read("config_server.ini")
choices = config.sections()
if len(choices) < 5:
	choices.append("New")
choices.append("Temp. profile")
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
mvaddstr(0, 0, "Use the arrow keys to navigate, press enter to select.")
mvaddstr(1, 0, "Select a pre-existing configuration profile, or create a new profile")
mvaddstr(2, 0, 'Select "Temp. profile" to make a new profile, without saving it')

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
    profile,port,max_population,root_pass = make_new_profile(config)
elif profile == "Manual":
    network_protocol,port,max_population,root_pass = make_temp_profile(config)
else:
    network_protocol=str(config[profile]["network_protocol"])
    port=int(config[profile]["port"])
    max_population=int(config[profile]["max_population"])
    root_pass=str(config[profile]["root_pass"])
version="0.2.0.1"
host='0.0.0.0'
serverIP="placeholder4serverIP"
client_handlers=[]
cmh = CommonMessageHoster()
lock = threading.Lock()
thread_manager = threading.Condition(lock) #tänk att detta är en manager som trådarna måste ha närvanade när det gör saker
taken_usernames=dict()
taken_usernames["SERVER"]=True
help=""
root_help="ADMIN COMMANDS:"
server_help="\nSEVER COMMANDS:"
command_dict={"/help":"View this message.",
              "/me":"Works like the irc command"}
root_command_dict={"/users":"Returns a list of all connected users",
                   "/users -show":"Sends a list of all connected users, to all connected users",
                   "/kick [username]":"Kicks the specified user.",
                   "/terminate":"Terminates the server"}
server_command_dict={"/promote [user]":"Grants [user] admin rights",
                     "/demote [user]":"Removes admin rights from [user]"}

for command in command_dict:
    help+=command+" "*(20-len(command))+command_dict[command]+"\n"
for command in root_command_dict:
    root_help+="\n"+command+" "*(20-len(command))+root_command_dict[command]
for command in server_command_dict:
    server_help+="\n"+command+" "*(20-len(command))+server_command_dict[command]

logbox=newwin(27,90,0,0)
logwin=newwin(24,88,1,1)
inpbox=newwin(3,90,27,0)
inpwin=newwin(1,85,28,4)
box(logbox,0,0)
box(inpbox,0,0)
mvwaddstr(inpbox,1,1,">>>")
scrollok(logwin,1)
wrefresh(logbox)
wrefresh(inpbox)
refresh()



if __name__ == "__main__":
    
    server = ThreadedTCPServer((host, port), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = False
    server_thread.start()
    waddstr(logwin, str("Running Dolpin v"+version+
                        "\nMax population not implemented yet."+
                        "\nListening @ "+serverIP+":"+str(port)+
                        "\nRoot password is: "+root_pass))
    wrefresh(logwin)
    
    serverinput=threading.Thread(target=server_input,daemon=True)
    serverinput.start()
    







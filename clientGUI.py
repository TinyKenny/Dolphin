import tkinter.messagebox
from tkinter import *
import socket
import os
import threading
import configparser
import time

class GUI:
    def print_to_log(self, msg):
        self.msg_log.insert(END, msg)
        if self.msg_log.size() > 30:
            self.msg_log.yview_scroll(1, UNITS)

    def read_input(self):  # that bitch .bind() wannts to pass the event(the key press) so i have to take it
        if self.user_input.get() == '':
            return 0
        self.print_to_log(self.user_input.get())
        self.user_input.set("")

    def __init__(self, window):
        window.title("Dolphin")
        self.toolbar_frame = Frame(window, bg="grey")  # the toolbar frame
        self.toolbar_frame.pack(side=TOP, fill=X)

        self.right_hand_frame = Frame(window)  # splits the rest of the window in two
        self.right_hand_frame.pack(side=RIGHT, fill=Y)
        self.left_hand_frame = Frame(window, bg="blue")
        self.left_hand_frame.pack(side=LEFT, fill=Y)

        self.info_frame = LabelFrame(self.right_hand_frame,  # creates the info frame
                                     text="Connection information",
                                     fg="black")
        self.info_frame.pack(pady=5, padx=5)

        self.ad_frame = Frame(self.right_hand_frame, bg="black")  # the advertisment frame (optinal)
        self.ad_frame.pack(side=BOTTOM)
        self.entry_frame = Frame(self.left_hand_frame)
        self.entry_frame.pack(side=BOTTOM, fill=X)  # user input frame

        self.log_frame = Frame(self.left_hand_frame)  # the log and log scroll frame
        self.log_frame.pack(side=LEFT, fill=Y)

        self.entry_marking = Label(self.entry_frame, text=">>>")  # the 3 arrows
        self.entry_marking.pack(side=LEFT)

        self.scroll = Scrollbar(self.log_frame, orient=VERTICAL)  # scroller
        self.scroll.pack(side=RIGHT, fill=Y, pady=5)

        self.log = StringVar()  # holds the data for the log widow
        self.msg_log = Listbox(self.log_frame,  # the logframe
                               height=30, width=100,
                               bg="white",
                               selectbackground="white",
                               selectforeground="black",
                               selectmode=SINGLE,
                               activestyle=NONE,
                               listvariable=self.log,
                               exportselection=0,
                               highlightbackground="grey",
                               yscrollcommand=self.scroll.set)  # text thing
        self.msg_log.pack(padx=5, pady=5, side=LEFT)
        self.scroll['command'] = self.msg_log.yview

        self.user_input = StringVar()
        self.entry = Entry(self.entry_frame,  # the input field
                           width=95,
                           highlightbackground="blue",
                           bg="white",
                           exportselection=0,
                           textvariable=self.user_input)

        def entry_event_handler(event, self=self):
            self.read_input()

        # the entry.bind() below insists to pass the event argument in the first variable slot
        # even if the first one is "self"
        # in order to allow the "self" argument to  be taken in the second slot is has to be done like this
        # TL:DR python is stupid

        self.entry.bind('<Return>', entry_event_handler)  # makes enter key send message
        self.entry.pack(padx=5, pady=5, side=LEFT)

        self.info_keys_color = "#595959"
        self.info_keys = [Label(self.info_frame, text="Server name:", fg=self.info_keys_color),
                          Label(self.info_frame, text="IP:", fg=self.info_keys_color)]

        self.info_values = [Label(self.info_frame, text="Pewds h8 club", fg=self.info_keys_color),
                            Label(self.info_frame, text="127.0.0.1", fg=self.info_keys_color)]

        self.ad = Label(self.ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5)
        self.ad.pack(padx=5, pady=5)

        for n in range(len(self.info_keys)):
            self.info_values[n].grid(row=n, column=0, sticky=E)
            self.info_values[n].grid(row=n, column=1, sticky=W)

        # TOOLBAR BUTTONS
        profile_butt = Button(self.toolbar_frame, text="Profiles")
        settings_butt = Button(self.toolbar_frame, text="Settings")
        change_butt = Button(self.toolbar_frame, text="Change Server")
        diconn_butt = Button(self.toolbar_frame, text="Disconnect")

        profile_butt.pack(side=LEFT, padx=3, pady=2)
        settings_butt.pack(side=LEFT, padx=3, pady=2)
        change_butt.pack(side=LEFT, padx=3, pady=2)
        diconn_butt.pack(side=LEFT, padx=3, pady=2)

def spacer(spaces, string):
    return (spaces - len(string)) * " "

def send_messages():  # the function that sends messages
    while True:
        client_message = input(">>>")
        if client_message[0:1] == "/":
            if command_interpreter(client_message):  # lauches command intepreter
                s.close()
                os._exit(0)
        else:
            s.send(str.encode(client_message))  # was not a command

def recieve_messages():  # the function that recieves messages
    try:
        while True:
            server_message = s.recv(2048).decode('utf-8')
            if not server_message:
                raise ConnectionError  # meddelandet är tomt, linux har lite svårt att fatta när det är dags att gå hem annars
            gui_obj.print_to_log(gui_obj, server_message)
    except ConnectionError as e:  # this will happen when the server is shut down
        gui_obj.print_to_log(gui_obj, ("Disconnected from:" + chat_server))

global gui_obj
def start_gui():
    window = Tk()  # creates the main window
    global gui_obj
    gui_obj = GUI(window) #make this cunt global
    window.mainloop()

def select_profile():
    prof_sel = Tk()
    prof_sel.title("Select Profile")
    frame = Frame(prof_sel)
    profile_list=["maual", "pewds h8 club"]
    prof_sel.mainloop()

gui_thread = threading.Thread(target=start_gui)
gui_thread.start()
time.sleep(1)
gui_obj.print_to_log("Version 0.0.0.1")

#select_profile()

chat_server=""
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

gui_obj.print_to_log("Select a proile to use or select manual:")
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
else: #profilen fannns inte
	print("No such porfile:" + profile +  "\n" +
		  "fine, fine, lemme just select \"default\" 4 u u lazy cunt")
	profile = "default"
	network_protocol = str(config[profile]["network_protocol"])
	if network_protocol == "IPv4":
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	elif network_protocol == "IPv6":
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
	developer_mode = config.getboolean(profile, "developer_mode", fallback=False)

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
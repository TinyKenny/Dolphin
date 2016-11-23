import tkinter.messagebox
from tkinter import *
import socket
import os
import threading
import configparser
import time

version="Version 0.0.0.2"

class GUI:
    def spacer(self, spaces, string):
        return (spaces - len(string)) * " "

    def command_interpreter(self, client_message):
        if client_message == "/quit":
            self.print_to_log("Disconnecting...")
            self.s.close()

        elif client_message == "/help":
            for command, desc in self.command_dict.items():
                self.print_to_log(command + desc)
            self.s.send(str.encode(client_message))

        elif client_message[0:6] == "/save ":
            configEditor = configparser.RawConfigParser()

            for profile in config.sections():  # lägga till de gamla profilerna i den nya filen
                configEditor.add_section(profile)
                configEditor.set(profile, "ip", config[profile]["ip"])
                configEditor.set(profile, "port", config[profile]["port"])
                configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
                configEditor.set(profile, "username", config[profile]["username"])
                if developer_mode:
                    configEditor.set(profile, "developer_mode", "True")

            # lägga till den nya profilen till filen
            prof_name = client_message[6:]
            configEditor.add_section(prof_name)
            configEditor.set(prof_name, "ip", chat_server)
            configEditor.set(prof_name, "port", str(port))
            configEditor.set(prof_name, "network_protocol", network_protocol)
            configEditor.set(prof_name, "username", username)
            if developer_mode:
                configEditor.set(prof_name, "developer_mode", "True")

            with open('profiles.ini', 'w') as new_configfile:
                configEditor.write(new_configfile)
                config.read("profiles.ini")
                self.print_to_log("Done!")

        elif client_message[0:5] == "/del ":
            if not (client_message[5:] in config.sections()):
                self.print_to_log("No such profile:" + client_message[5:])
                return 0

            configEditor = configparser.RawConfigParser()

            for profile in config.sections():  # lägga till de gamla profilerna i den nya filen
                if profile == client_message[5:]:
                    continue
                configEditor.add_section(profile)
                configEditor.set(profile, "ip", config[profile]["ip"])
                configEditor.set(profile, "port", config[profile]["port"])
                configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
                configEditor.set(profile, "username", config[profile]["username"])
                if developer_mode:
                    configEditor.set(profile, "developer_mode", "True")

            with open('profiles.ini', 'w') as new_configfile:
                configEditor.write(new_configfile)
                config.read("profiles.ini")  # detta fungerar inte, ingen aning om varför, kan inte hitta en lösning
                self.print_to_log("Done!")

        elif client_message[0:11] == "/edit -all ":
            if not (client_message[11:] in config.sections()):
                self.print_to_log("No such profile:" + client_message[16:])
                return 0

            configEditor = configparser.RawConfigParser()

            for profile in config.sections():  # lägga till profilerna i den nya filen
                if profile == client_message[11:]:  # den som ska ändas har hittats
                    self.print_to_log("Current name:" + profile)
                    new_profile_name = input("Enter new name:\n>>>")
                    configEditor.add_section(new_profile_name)
                    self.print_to_log("Current IP:" + config[profile]["ip"])
                    configEditor.set(new_profile_name, "ip", input("Enter new IP addres:\n>>>"))
                    self.print_to_log("Current port:" + str(config[profile]["port"]))
                    configEditor.set(new_profile_name, "port", input("Enter new port:\n>>>"))
                    self.print_to_log("Current network protocol:" + config[profile]["network_protocol"])
                    configEditor.set(new_profile_name, "network_protocol", input("Enter new network protocol:\n>>>"))
                    self.print_to_log("Current username:" + config[profile]["username"])
                    configEditor.set(new_profile_name, "username", input("Enter new username:\n>>>"))
                    if developer_mode:
                        if not input("Enter new dev mode status(True/False)\n>>>") == "False":
                            configEditor.set(new_profile_name, "developer_mode", True)
                else:  # detta var inte profilen som skulle ändras, lägger till den som den är i den nya filen
                    configEditor.add_section(profile)
                    configEditor.set(profile, "ip", config[profile]["ip"])
                    configEditor.set(profile, "port", config[profile]["port"])
                    configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
                    configEditor.set(profile, "username", config[profile]["username"])
                    try:
                        if config[profile]["developer_mode"]:
                            configEditor.set(profile, "developer_mode", "True")
                    except KeyError as e:
                        pass  # profilen var ej developer, inget ska hända

            with open('profiles.ini', 'w') as new_configfile:
                configEditor.write(new_configfile)
                config.read("profiles.ini")  # detta fungerar inte, ingen aning om varför, kan inte hitta en lösning

        elif client_message[0:6] == "/edit ":
            if not (client_message[6:] in config.sections()):
                self.print_to_log("No such profile:" + client_message[6:])
                return 0

            configEditor = configparser.RawConfigParser()

            for profile in config.sections():  # lägga till profilerna i den nya filen
                if profile == client_message[6:]:  # den som ska ändas har hittats
                    self.print_to_log("Current name:" + profile)
                    new_profile_name = input("Enter new profile name:\n>>>")
                    configEditor.add_section(new_profile_name)
                    self.print_to_log("Current IP:" + config[profile]["ip"])
                    configEditor.set(new_profile_name, "ip", input("Enter new IP addres:\n>>>"))
                    configEditor.set(new_profile_name, "port", config[profile]["port"])  # sker auto
                    configEditor.set(new_profile_name, "network_protocol",
                                     config[profile]["network_protocol"])  # sker auto
                    self.print_to_log("Current username:" + config[profile]["username"])
                    configEditor.set(new_profile_name, "username", input("Enter new username:\n>>>"))
                    try:
                        if config[profile]["developer_mode"]:
                            configEditor.set(new_profile_name, "developer_mode", "True")
                    except KeyError as e:
                        pass  # profilen var ej developer, inget ska hända
                else:
                    configEditor.add_section(profile)
                    configEditor.set(profile, "ip", config[profile]["ip"])
                    configEditor.set(profile, "port", config[profile]["port"])
                    configEditor.set(profile, "network_protocol", config[profile]["network_protocol"])
                    configEditor.set(profile, "username", config[profile]["username"])
                    try:
                        if config[profile]["developer_mode"]:
                            configEditor.set(profile, "developer_mode", "True")
                    except KeyError as e:
                        pass  # profilen var ej developer, inget ska hända

            with open('profiles.ini', 'w') as new_configfile:
                configEditor.write(new_configfile)
                config.read("profiles.ini")  # detta fungerar inte, ingen aning om varför, kan inte hitta en lösning

        elif client_message == "/view -all":
            self.print_to_log("Profile name" + self.spacer(15, "Profile name") +
                  "IP addres" + self.spacer(13, "IP addres") +
                  "Port" + self.spacer(8, "port") +
                  "Network Protocol  " +
                  "Username")
            for profile in config.sections():
                self.print_to_log(profile +
                      (15 - len(profile)) * " " +
                      config[profile]["ip"] +
                      (13 - len(config[profile]["ip"])) * " " +
                      config[profile]["port"] +
                      (8 - len(config[profile]["port"])) * " " +
                      config[profile]["network_protocol"] +
                      (18 - len(config[profile]["network_protocol"])) * " " +
                      config[profile]["username"])

        elif client_message == "/view":
            self.print_to_log("Profile name" + self.spacer(15, "Profile name") +
                  "IP addres" + self.spacer(13, "IP addres") +
                  "Username")
            for profile in config.sections():
                self.print_to_log(profile +
                      (15 - len(profile)) * " " +
                      config[profile]["ip"] +
                      (13 - len(config[profile]["ip"])) * " " +
                      config[profile]["username"])

        else:
            self.s.send(str.encode(client_message))

    def recieve_messages(self):  # the function that recieves messages
        try:
            while True:
                server_message = self.s.recv(2048).decode('utf-8')
                if not server_message:
                    raise ConnectionError  # meddelandet är tomt, linux har lite svårt att fatta när det är dags att gå hem annars
                self.print_to_log(server_message)
        except ConnectionError as e:  # this will happen when the server is shut down
            self.print_to_log("Disconnected from:" + chat_server.get())

    def print_to_log(self, msg):
        self.msg_log.insert(END, msg)
        if self.msg_log.size() > 30:
            self.msg_log.yview_scroll(1, UNITS)

    def read_input(self):  #does not work work woth server
        if self.user_input.get() == '':
            return 0
        try:
            if self.user_input.get()[0:1] == "/":
                self.command_interpreter(self.user_input.get())  # lauches command intepreter
            else:
                self.s.send(str.encode(self.user_input.get()))  # was not a comman

        except OSError:#not connectde to a sever
            self.print_to_log(self.user_input.get())
        except AttributeError:
            self.print_to_log(self.user_input.get())#same
        finally:
            self.user_input.set("")

    def manual_connect(self):
        connet_window=Tk()
        connet_window.title("Manual Connect")
        #username
        Label(connet_window, text="Username").grid(row=0, column=0, sticky='E')
        username_field=Entry(connet_window,
                         width=16,
                         exportselection=0,
                         textvariable= self.username,
                         bg="white")
        username_field.grid(row=0, column=1, sticky='W', pady=2)

        #ip
        Label(connet_window, text="IP adresss").grid(row=1, column=0, sticky='E')
        chat_server_field=Entry(connet_window,
                              width=16,
                              exportselection=0,
                              textvariable=self.chat_server,
                              bg="white")
        chat_server_field.grid(row=1, column=1, pady=2)

        #port
        Label(connet_window, text="Port").grid(row=2, column=0, sticky='E')
        port_field=Entry(connet_window,
                         width=5,
                         exportselection=0,
                         textvariable=self.port,
                         bg="white")
        port_field.grid(row=2, column=1, sticky='W', pady=2)

        #network protocol
        def setIPv4():
            self.network_protocol.set("IPv4")

        def setIPv6():
            self.network_protocol.set("IPv6")
        network_protocol_frame=LabelFrame(connet_window, text="Network Protocol")
        network_protocol_frame.grid(row=3, columnspan=2, pady=2)
        ipv4_butt = Radiobutton(network_protocol_frame,
                                text="IPv4", variable=self.network_protocol,
                                value='IPv4',
                                command=setIPv4)
        ipv4_butt.grid()
        ipv4_butt.select()
        ipv6_butt = Radiobutton(network_protocol_frame,
                                text="IPv6",
                                variable=self.network_protocol,
                                value='IPv6',
                                command=setIPv6)
        ipv6_butt.grid()

        #buttons frame
        def cancel():
            self.username.set('')
            self.chat_server.set('')
            self.port.set('')
            self.network_protocol.set('')
            connet_window.destroy()

        def connect():
            '''print(self.username.get())
            print(self.network_protocol.get())
            print(self.chat_server.get())
            print(self.port.get())'''
            if self.chat_server.get()=="":
                self.username.set("bob")
                self.port.set(5555)
                self.chat_server.set("127.0.0.1")
                ipv4_butt.invoke() #sätter IPv4
            self.connect()
            connet_window.destroy()

        butt_frame=Frame(connet_window)
        butt_frame.grid(row=4, columnspan=2, pady=4)
        connect_butt=Button(butt_frame,
                            text="Connect",
                            fg='green',
                            activeforeground='green',
                            command=connect)
        cancel_butt=Button(butt_frame,
                           text="Cancel",
                           fg='red',
                           activeforeground='red',
                           command=cancel)
        connect_butt.pack(side=LEFT)
        cancel_butt.pack(side=RIGHT)

        connet_window.mainloop()

    def disconnect(self):
        print("Disconnecting...")
        self.s.close()
        self.c_or_dc.set("Connect")
        pass

    def connect(self):
        if self.network_protocol.get() == "IPv4":
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.network_protocol.get() == "IPv6":
            self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.print_to_log("Corrupt profile or invalid input")
        try:
            self.s.connect((self.chat_server.get(), self.port.get()))
            self.print_to_log(("Connected to: " + self.chat_server.get() + ":" + str(self.port.get())))
            data = self.s.recv(2048)  # recieve the message of the day
            self.print_to_log("Message of the day: " + str(data.decode('utf-8')))  # currently just a random quote
            self.s.send(str.encode(self.username.get()))  # inform the server of your username
        except socket.error as e:  # couldn't connect to given IP + port
            self.print_to_log(("Cound not connect to", self.chat_server.get() + ":" + str(self.port.get()) + "\n" + str(e)))

        reciever = threading.Thread(target=self.recieve_messages, daemon=0)
        reciever.start()
        self.c_or_dc.set("Disconnect")

    def build_window(self, window):
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
                               highlightbackground="black",
                               yscrollcommand=self.scroll.set)  # text thing
        self.msg_log.pack(padx=5, pady=5, side=LEFT)
        self.scroll['command'] = self.msg_log.yview

        self.user_input = StringVar()
        self.entry = Entry(self.entry_frame,  # the input field
                           width=95,
                           highlightbackground="black",
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

        info_keys_color = "black"
        self.info_keys = [Label(self.info_frame, text="Server name:", fg=info_keys_color),
                          Label(self.info_frame, text="IP:", fg=info_keys_color),
                          Label(self.info_frame, text="Username:", fg=info_keys_color),
                          Label(self.info_frame, text="Level:", fg=info_keys_color),]

        self.info_values = [Label(self.info_frame, text="placeholder", fg=info_keys_color),
                            Label(self.info_frame, textvariable=self.chat_server, fg=info_keys_color),
                            Label(self.info_frame, textvariable=self.username, fg=info_keys_color),
                            Label(self.info_frame, text="placeholder", fg=info_keys_color)]

        for n in range(len(self.info_keys)):
            self.info_keys[n].grid(row=n, column=0, sticky=E)
            self.info_values[n].grid(row=n, column=1, sticky=W)

        self.ad = Label(self.ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5)
        self.ad.pack(padx=5, pady=5)

        # TOOLBAR BUTTONS
        def conn_or_disconn():
            if self.c_or_dc.get() == "Connect":
                self.manual_connect()
            elif self.c_or_dc.get() == "Disconnect":
                self.disconnect()

        self.c_or_dc = StringVar()
        self.c_or_dc.set("Connect")
        connect_butt = Button(self.toolbar_frame,
                              textvariable=self.c_or_dc,
                              command=conn_or_disconn)
        profile_butt = Button(self.toolbar_frame, text="Profiles")
        settings_butt = Button(self.toolbar_frame, text="Settings")

        connect_butt.pack(side=LEFT, padx=3, pady=2)
        profile_butt.pack(side=LEFT, padx=3, pady=2)
        settings_butt.pack(side=LEFT, padx=3, pady=2)

    def __init__(self, window):

        self.chat_server = StringVar()
        self.port = IntVar()
        self.username = StringVar()
        self.network_protocol = StringVar()
        self.config = configparser.ConfigParser()
        self.config.read("profiles.ini")

        self.command_dict = {"/help": self.spacer(20, "/help") + "view this page",
                        "/quit": self.spacer(20, "/quit") + "exit program",
                        "/save [name]": self.spacer(20, "/save [name]") + "save profile settings as [name]",
                        "/del [name]": self.spacer(20, "/del [name]") + "delete profile [name]",
                        "/view": self.spacer(20, "/view") + "views your saved profiles",
                        "/edit [name]": self.spacer(20, "/edit [name]") + "edit profile [name]",
                        "/edit -all [name]": self.spacer(20, "/edit -all [name]") + "edit all avalible information about profile [name]",
                        "/view -all": self.spacer(20, "/view -all") + "views all inofmation avalible about you profiles"}

        self.build_window(window)

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

while 1: #annars hinner inte föstret skapas innan nästa rad och då blir det error
    try:
        gui_obj.print_to_log(version)
        break
    except NameError:
        pass

chat_server=""
port=5555
developer_mode=0
config = configparser.ConfigParser()
config.read("profiles.ini")
network_protocol=""

print("Select a proile to use or select manual:")
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


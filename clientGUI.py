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
        return ((spaces - len(string)) * " ")

    def new_profile(self):
        self.print_to_log("new profile")

    def edit_profiles(self):
        self.print_to_log("edit profile")

    def use_profile(self):
        use_profile_window = Tk()
        use_profile_window.title("Select profile")

        config = configparser.ConfigParser()
        config.read("profiles.ini")

        scroll = Scrollbar(use_profile_window, orient=VERTICAL)  # scroller
        scroll.grid(row=0, column=0, pady=3, sticky='E')

        selections = StringVar()


        selection_box = Listbox(use_profile_window,
                                bg="white",
                                width=10,
                                height=5,
                                selectmode=SINGLE,
                                exportselection=0,
                                yscrollcommand=scroll.set,
                                listvariable=selections,#FUCKING BS PYTHON IGNORES THIS LINE
                                activestyle=NONE)
        scroll['command'] = selection_box.yview
        selection_box.grid(row=0, column=1, sticky='W')

        selection_box.insert(END, "Manual")
        selections_list = []
        for sel in config.sections():
            selection_box.insert(END, sel)
            selections_list.append(sel)

        # buttons
        def cancel():
            use_profile_window.destroy()

        def connect():
            if str(selection_box.curselection()) == "()":
                return 0
            elif str(selection_box.curselection()) == "(0,)":
                use_profile_window.destroy()
            else:
                selected_profile = selections_list[int(str(selection_box.curselection())[1:-2]) - 1]
                print(type(selected_profile))
                self.username.set(config[selected_profile]["username"])
                self.port.set(config[selected_profile]["port"])
                self.chat_server.set(config[selected_profile]["ip"])
                self.network_protocol.set(config[selected_profile]["network_protocol"])
                use_profile_window.destroy()
                self.connect()

        butt_frame = Frame(use_profile_window)
        butt_frame.grid(row=1, columnspan=2, pady=4, padx=4)
        connect_butt = Button(butt_frame,
                              text="Connect",
                              fg='green',
                              activeforeground='green',
                              command=connect)
        cancel_butt = Button(butt_frame,
                             text="Cancel",
                             fg='red',
                             activeforeground='red',
                             command=cancel)
        connect_butt.pack(side=LEFT, padx=2)
        cancel_butt.pack(side=RIGHT)

        use_profile_window.mainloop()

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

            for profile in self.config.sections():  # lägga till de gamla profilerna i den nya filen
                configEditor.add_section(profile)
                configEditor.set(profile, "ip", self.config[profile]["ip"])
                configEditor.set(profile, "port", self.config[profile]["port"])
                configEditor.set(profile, "network_protocol", self.config[profile]["network_protocol"])
                configEditor.set(profile, "username", self.config[profile]["username"])
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
                self.config.read("profiles.ini")
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
            self.print_to_log("Disconnected from: " + self.chat_server.get())
            self.chat_server.set('')

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
        port_field.insert(END, "5555")

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
            ''''print(self.username.get())
            print(self.network_protocol.get())
            print(self.chat_server.get())
            print(self.port.get())'''
            if self.chat_server.get()=="":
                self.username.set("bob")
                self.port.set(5555)
                self.chat_server.set("127.0.0.1")
                ipv4_butt.invoke() #sätter IPv4
            else:
                self.username.set(username_field.get())
                #network protocol is alredy set
                self.chat_server.set(chat_server_field.get())
                self.port.set(port_field.get())
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
        self.s.close()
        self.username.set('')
        #self.chat_server.set('') this is done in self.recieve_messages()
        self.port.set('')
        self.network_protocol.set('')
        self.c_or_dc.set("Connect")

    def connect(self):
        if self.network_protocol.get() == "IPv4":
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif self.network_protocol.get() == "IPv6":
            self.s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            self.print_to_log("Corrupt profile or invalid input")
        try:
            self.s.connect((self.chat_server.get(), self.port.get()))
            self.print_to_log(("Connected to: " + self.chat_server.get()))
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
        toolbar_frame = Frame(window, bg="grey")  # the toolbar frame
        toolbar_frame.pack(side=TOP, fill=X)

        right_hand_frame = Frame(window)  # splits the rest of the window in two
        right_hand_frame.pack(side=RIGHT, fill=Y)
        left_hand_frame = Frame(window, bg="blue")
        left_hand_frame.pack(side=LEFT, fill=Y)

        info_frame = LabelFrame(right_hand_frame,  # creates the info frame
                                     text="Connection information",
                                     fg="black")
        info_frame.pack(pady=5, padx=5)

        ad_frame = Frame(right_hand_frame, bg="black")  # the advertisment frame (optinal)
        ad_frame.pack(side=BOTTOM)
        entry_frame = Frame(left_hand_frame)
        entry_frame.pack(side=BOTTOM, fill=X)  # user input frame

        log_frame = Frame(left_hand_frame)  # the log and log scroll frame
        log_frame.pack(side=LEFT, fill=Y)

        entry_marking = Label(entry_frame, text=">>>")  # the 3 arrows
        entry_marking.pack(side=LEFT)

        scroll = Scrollbar(log_frame, orient=VERTICAL)  # scroller
        scroll.pack(side=RIGHT, fill=Y, pady=5)

        self.log = StringVar()  # holds the data for the log widow
        self.msg_log = Listbox(log_frame,  # the logframe
                               height=30, width=100,
                               bg="white",
                               selectbackground="white",
                               selectforeground="black",
                               selectmode=SINGLE,
                               activestyle=NONE,
                               listvariable=self.log,
                               exportselection=0,
                               highlightbackground="black",
                               yscrollcommand=scroll.set)  # text thing
        self.msg_log.pack(padx=5, pady=5, side=LEFT)
        scroll['command'] = self.msg_log.yview

        self.user_input = StringVar()
        entry = Entry(entry_frame,  # the input field
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

        entry.bind('<Return>', entry_event_handler)  # makes enter key send message
        entry.pack(padx=5, pady=5, side=LEFT)

        info_keys_color = "black"
        info_keys = [Label(info_frame, text="Server name:", fg=info_keys_color),
                          Label(info_frame, text="IP:", fg=info_keys_color),
                          Label(info_frame, text="Username:", fg=info_keys_color),
                          Label(info_frame, text="Level:", fg=info_keys_color),]

        info_values = [Label(info_frame, text="placeholder", fg=info_keys_color),
                            Label(info_frame, textvariable=self.chat_server, fg=info_keys_color),
                            Label(info_frame, textvariable=self.username, fg=info_keys_color),
                            Label(info_frame, text="placeholder", fg=info_keys_color)]

        for n in range(len(info_keys)):
            info_keys[n].grid(row=n, column=0, sticky=E)
            info_values[n].grid(row=n, column=1, sticky=W)

        ad = Label(ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5)
        ad.pack(padx=5, pady=5)

        # TOOLBAR BUTTONS
        def conn_or_disconn():
            if self.c_or_dc.get() == "Connect":
                self.manual_connect()
            elif self.c_or_dc.get() == "Disconnect":
                self.disconnect()

        self.c_or_dc = StringVar()
        self.c_or_dc.set("Connect")
        connect_butt = Button(toolbar_frame,
                              textvariable=self.c_or_dc,
                              command=conn_or_disconn)

        profile_butt = Menubutton(toolbar_frame,
                                  text="Profiles",
                                  relief=RAISED, bd=2)
        profile_butt.menu=Menu(profile_butt, tearoff=0)
        profile_butt.menu.add_command(label='New', command=self.new_profile)
        profile_butt.menu.add_command(label='Edit', command=self.edit_profiles)
        profile_butt.menu.add_command(label='Use', command=self.use_profile)
        profile_butt['menu']=profile_butt.menu
        settings_butt = Button(toolbar_frame, text="Settings")

        connect_butt.pack(side=LEFT, padx=3, pady=2)
        profile_butt.pack(side=LEFT, padx=3, pady=2)
        settings_butt.pack(side=LEFT, padx=3, pady=2)

    def __init__(self, window):

        self.chat_server = StringVar()
        self.port = IntVar()
        self.username = StringVar()
        self.network_protocol = StringVar()

        self.command_dict = {"/help": self.spacer(20, "/help") + "view this page",
                        "/quit": self.spacer(20, "/quit") + "exit program",
                        "/save [name]": self.spacer(20, "/save [name]") + "save profile settings as [name]",
                        "/del [name]": self.spacer(20, "/del [name]") + "delete profile [name]",
                        "/view": self.spacer(20, "/view") + "views your saved profiles",
                        "/edit [name]": self.spacer(20, "/edit [name]") + "edit profile [name]",
                        "/edit -all [name]": self.spacer(20, "/edit -all [name]") + "edit all avalible information about profile [name]",
                        "/view -all": self.spacer(20, "/view -all") + "views all inofmation avalible about you profiles"}

        self.build_window(window)

print("wall")
window = Tk()  # creates the main window
gui_obj = GUI(window) #make this cunt global
window.mainloop()
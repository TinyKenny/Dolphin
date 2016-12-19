import tkinter.messagebox
from tkinter import font
from tkinter import *
import socket
import os
import threading
import configparser
import time

version="Version 0.0.1.2 ALPHA"
global gui_obj #make this cunt global so that it can be used in ProfileButtons

class ProfileButtons:
    index=-1
    label=""

    def get_index(self):
        return self.index

    def __init__(self, index, label):
        self.index=index
        self.label=label


    def call(self):
        profiles = configparser.ConfigParser()
        profiles.read("profiles.ini")
        gui_obj.chat_server.set(profiles[self.label]["ip"])
        gui_obj.network_protocol.set(profiles[self.label]["network_protocol"])
        gui_obj.port.set(profiles[self.label]["port"])
        gui_obj.username.set(profiles[self.label]["username"])
        gui_obj.connect()
        """
        när man klickar på "default" så kommer knappen att ropa på element [n] i knapp listan
        detta kommer att köra "call()"
        call() sätter alla värden
        call() kallar connect()
        """

class GUI:
    def spacer(self, spaces, string):
        return ((spaces - len(string)) * " ")

    def new_profile(self):
        new_profile_window = Tk()
        new_profile_window.title("New Profile")
        new_profile_window.configure(bg=self.bg_color)

        #profile name
        Label(new_profile_window,
              text="Profile Name",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=0, column=0, sticky='E')
        name_field = Entry(new_profile_window,
                           width=16,
                           exportselection=0,
                           bg="white")
        name_field.grid(row=0, column=1, sticky='W', pady=2)

        # username
        Label(new_profile_window,
              text="Username",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=1, column=0, sticky='E')
        username_field = Entry(new_profile_window,
                               width=16,
                               exportselection=0,
                               textvariable=self.username,
                               bg="white")
        username_field.grid(row=1, column=1, sticky='W', pady=2)
        username_field.insert(END, self.username.get())

        # ip
        Label(new_profile_window,
              text="IP adresss",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=2, column=0, sticky='E')
        chat_server_field = Entry(new_profile_window,
                                  width=16,
                                  exportselection=0,
                                  textvariable=self.chat_server,
                                  bg="white")
        chat_server_field.grid(row=2, column=1, pady=2)
        chat_server_field.insert(END, self.chat_server.get())

        # port
        Label(new_profile_window,
              text="Port",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=3, column=0, sticky='E')
        port_field = Entry(new_profile_window,
                           width=5,
                           exportselection=0,
                           textvariable=self.port,
                           bg="white")
        port_field.grid(row=3, column=1, sticky='W', pady=2)
        if self.port.get()==0:
            port_field.insert(END, 5555)
        else:
            port_field.insert(END, self.port.get())

        # network protocol
        network_protocol = StringVar()
        def setIPv4():
            network_protocol.set("IPv4")

        def setIPv6():
            network_protocol.set("IPv6")

        network_protocol_frame = LabelFrame(new_profile_window,
                                            text="Network Protocol",
                                            bg=self.bg_color,
                                            fg=self.foreground_color)
        network_protocol_frame.grid(row=4, columnspan=2, pady=2)
        ipv4_butt = Radiobutton(network_protocol_frame,
                                text="IPv4", variable=network_protocol,
                                value='IPv4',
                                command=setIPv4,
                                bg=self.bg_color,
                                fg=self.foreground_color)
        ipv4_butt.grid()
        ipv4_butt.select()

        ipv6_butt = Radiobutton(network_protocol_frame,
                                text="IPv6",
                                variable=network_protocol,
                                value='IPv6',
                                command=setIPv6,
                                bg=self.bg_color,
                                fg=self.foreground_color)
        ipv6_butt.grid()

        if self.network_protocol.get() == "IPv6":
        #loads the selected network protocol
            ipv6_butt.invoke()
        else:
            ipv4_butt.invoke()


        # buttons frame
        def cancel():
            new_profile_window.destroy()

        def create():
            if (name_field.get()=="") | (chat_server_field.get()=="") | (port_field.get()==0) | (network_protocol.get()=="") | (username_field.get()==""):
                #ensures that no field is empty
                return 0
            profiles = configparser.ConfigParser()
            profiles.read("profiles.ini")
            profiles.add_section(name_field.get())
            profiles.set(name_field.get(), "ip", chat_server_field.get())
            profiles.set(name_field.get(), "port", port_field.get())
            profiles.set(name_field.get(), "network_protocol", network_protocol.get())#this is a StringVar
            profiles.set(name_field.get(), "username", username_field.get())

            try:
                with open('profiles.ini', 'w') as new_configfile:
                    profiles.write(new_configfile)
                    self.add_profile_to_butt_cascade(name_field.get())
                    tkinter.messagebox.showinfo("Saved", "Saved Successfully")
            except:
                tkinter.messagebox.showerror("Error", "Could not save")


            new_profile_window.destroy()

        butt_frame = Frame(new_profile_window, bg=self.bg_color)
        butt_frame.grid(row=5, columnspan=2, pady=4)
        connect_butt = Button(butt_frame,
                              text="Save",
                              fg='#86FF59',
                              activeforeground='green',
                              command=create,
                              bg=self.butt_color,
                              activebackground=self.active_butt_color)
        cancel_butt = Button(butt_frame,
                             text="Cancel",
                             fg='#FA4854',
                             activeforeground='red',
                             command=cancel,
                             bg=self.butt_color,
                             activebackground=self.active_butt_color)
        connect_butt.pack(side=LEFT, padx=5)
        cancel_butt.pack(side=RIGHT)

        new_profile_window.mainloop()

    def edit_specific_profile(self, profile_name, username, ip, port, network_protocol_string):
        new_profile_window = Tk()
        new_profile_window.title("Edit Profile")
        new_profile_window.configure(bg=self.bg_color)

        #profile name
        Label(new_profile_window,
              text="Profile Name",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=0, column=0, sticky='E')
        name_field = Entry(new_profile_window,
                           width=16,
                           exportselection=0,
                           bg="white")
        name_field.grid(row=0, column=1, sticky='W', pady=2)
        name_field.insert(END, profile_name)

        # username
        Label(new_profile_window,
              text="Username",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=1, column=0, sticky='E')
        username_field = Entry(new_profile_window,
                               width=16,
                               exportselection=0,
                               textvariable=self.username,
                               bg="white")
        username_field.grid(row=1, column=1, sticky='W', pady=2)
        username_field.insert(END, username)

        # ip
        Label(new_profile_window,
              text="IP adresss",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=2, column=0, sticky='E')
        chat_server_field = Entry(new_profile_window,
                                  width=16,
                                  exportselection=0,
                                  textvariable=self.chat_server,
                                  bg="white")
        chat_server_field.grid(row=2, column=1, pady=2)
        chat_server_field.insert(END, ip)

        # port
        Label(new_profile_window,
              text="Port",
              bg=self.bg_color,
              fg=self.foreground_color).grid(row=3, column=0, sticky='E')
        port_field = Entry(new_profile_window,
                           width=5,
                           exportselection=0,
                           textvariable=self.port,
                           bg="white")
        port_field.grid(row=3, column=1, sticky='W', pady=2)
        if self.port.get()==0:
            port_field.insert(END, 5555)
        else:
            port_field.insert(END, port)

        # network protocol
        network_protocol = StringVar()
        def setIPv4():
            network_protocol.set("IPv4")

        def setIPv6():
            network_protocol.set("IPv6")

        network_protocol_frame = LabelFrame(new_profile_window,
                                            text="Network Protocol",
                                            bg=self.bg_color,
                                            fg=self.foreground_color)
        network_protocol_frame.grid(row=4, columnspan=2, pady=2)
        ipv4_butt = Radiobutton(network_protocol_frame,
                                text="IPv4",
                                variable=network_protocol,
                                value='IPv4',
                                command=setIPv4,
                                bg=self.bg_color,
                                fg=self.foreground_color)
        ipv4_butt.grid()
        ipv4_butt.select()

        ipv6_butt = Radiobutton(network_protocol_frame,
                                text="IPv6",
                                variable=network_protocol,
                                value='IPv6',
                                command=setIPv6,
                                bg=self.bg_color,
                                fg=self.foreground_color)
        ipv6_butt.grid()

        if network_protocol_string == "IPv6":
        #loads the selected network protocol
            ipv6_butt.invoke()
        else:
            ipv4_butt.invoke()

        # buttons
        def cancel():
            new_profile_window.destroy()
            #needs to add the profile again since it was deleted

        def save():
            if (name_field.get()=="") | (chat_server_field.get()=="") | (port_field.get()==0) | (network_protocol.get()=="") | (username_field.get()==""):
                return 0
                #ensures that no field is empty

            profiles = configparser.ConfigParser()
            profiles.read("profiles.ini")

            self.remove_profile_from_butt_cascade(profile_name)#removes the old version
            profiles.remove_section(profile_name)#same

            profiles.add_section(name_field.get())
            profiles.set(name_field.get(), "ip", chat_server_field.get())
            profiles.set(name_field.get(), "port", port_field.get())
            profiles.set(name_field.get(), "network_protocol", network_protocol.get())#this is a StringVar, not an Entry object
            profiles.set(name_field.get(), "username", username_field.get())

            try:
                with open('profiles.ini', 'w') as new_configfile:
                    profiles.write(new_configfile)
                    self.add_profile_to_butt_cascade(name_field.get())
                    tkinter.messagebox.showinfo("Saved", "Saved Successfully")
            except:
                tkinter.messagebox.showerror("Error", "Could not save")
            new_profile_window.destroy()

        butt_frame = Frame(new_profile_window, bg=self.bg_color)
        butt_frame.grid(row=5, columnspan=2, pady=4)
        connect_butt = Button(butt_frame,
                              text="Save",
                              fg='#86FF59',
                              activeforeground='green',
                              command=save,
                              bg=self.butt_color,
                              activebackground=self.active_butt_color)
        cancel_butt = Button(butt_frame,
                             text="Cancel",
                             fg='#FA4854',
                             activeforeground='red',
                             command=cancel,
                             bg=self.butt_color,
                             activebackground=self.active_butt_color)
        connect_butt.pack(side=LEFT, padx=5)
        cancel_butt.pack(side=RIGHT)

        new_profile_window.mainloop()

    def edit_profiles(self):
        edit_profile_window=Tk()
        edit_profile_window.title("Edit Profile")
        edit_profile_window.configure(bg=self.bg_color)

        profiles_var=StringVar()
        select_profile=Listbox(edit_profile_window,
                               height=10, width=15,
                               bg="white",
                               selectmode=SINGLE,
                               activestyle=NONE,
                               listvariable=profiles_var,
                               exportselection=0,
                               highlightbackground="black")

        profiles = configparser.ConfigParser()
        profiles.read("profiles.ini")

        for n in profiles.sections():
            select_profile.insert(END, n)
        select_profile.pack(side=LEFT, padx=3, pady=3)

        the_rest_frame=Frame(edit_profile_window, bg=self.bg_color)
        the_rest_frame.pack(side=RIGHT, padx=3, pady=3)

        self.info_frame=LabelFrame(the_rest_frame, text="Info", bg=self.bg_color, fg=self.foreground_color)
        self.info_frame.pack(pady=3)

        test=Label(self.info_frame, text="Comming soon...", bg=self.bg_color, fg=self.foreground_color)
        test.grid(pady=3)

        def new():
            edit_profile_window.destroy()
            self.new_profile()

        def edit():
            try:
                profile_to_be_edited = profiles.sections()[select_profile.curselection()[0]]
            except IndexError:
                return 0
                #nothing was selected
            username = profiles.get(profile_to_be_edited, "username")
            ip = profiles.get(profile_to_be_edited, "ip")
            port = profiles.get(profile_to_be_edited, "port")
            network_protocol = profiles.get(profile_to_be_edited, "network_protocol")
            #mellanlagring är endast för att det ska bli lättare att skriva/läsa

            #delete()
            edit_profile_window.destroy()
            self.edit_specific_profile(profile_to_be_edited, username, ip, port, network_protocol)

        def delete():
            try:
                label=profiles.sections()[select_profile.curselection()[0]]
            except IndexError:
                return 0
                #nothing was selected
            profiles.remove_section(label)

            profiles.update()# vet ej vad denna gör men kan ej skada
            self.remove_profile_from_butt_cascade(label)
            select_profile.delete(select_profile.curselection()[0])
            select_profile.update()  # vet ej vad denna gör men kan ej skada

            with open('profiles.ini', 'w') as new_configfile:
                profiles.write(new_configfile)

        new_butt=Button(the_rest_frame,
                        text="New",
                        width=6,
                        fg=self.butt_fg_color,
                        activeforeground='white',
                        command=new,
                        bg=self.butt_color,
                        activebackground=self.active_butt_color)
        new_butt.pack(pady=3)

        edit_butt=Button(the_rest_frame,
                         text="Edit",
                         width=6,
                         fg=self.butt_fg_color,
                         activeforeground='white',
                         command=edit,
                         bg=self.butt_color,
                         activebackground=self.active_butt_color)
        edit_butt.pack(pady=3)

        delete_butt = Button(the_rest_frame,
                             text="Delete",
                             fg=self.butt_fg_color,
                             width=6,
                             activeforeground='white',
                             command=delete,
                             bg=self.butt_color,
                             activebackground=self.active_butt_color)
        delete_butt.pack(pady=3)

        #knappar: Edit, Delete, New
        #rutor: select, info

        edit_profile_window.mainloop()

    def settings(self):

        settings_window = Tk()
        settings_window.title("Settings")
        settings_window.config(bg=self.bg_color)

        settings = configparser.ConfigParser()
        settings.read("settings.ini")

        theme = configparser.ConfigParser()
        theme.read("theme.ini")

        show_errors_var = StringVar()

        def setYes():
            show_errors_var.set("Yes")

        def setNo():
            show_errors_var.set("No")

        show_errors_frame = LabelFrame(settings_window,
                                       text="Show error messages",
                                       bg=self.bg_color,
                                       fg=self.foreground_color)
        show_errors_frame.pack(pady=5, padx=5, fill=X)
        yes_butt = Radiobutton(show_errors_frame,
                               text="Yes",
                               variable=show_errors_var,
                               value="Yes",
                               command=setYes,
                               bg=self.bg_color,
                               fg=self.foreground_color)
        yes_butt.grid()

        no_butt = Radiobutton(show_errors_frame,
                              text="No",
                              variable=show_errors_var,
                              value='No',
                              command=setNo,
                              bg=self.bg_color,
                              fg=self.foreground_color)
        no_butt.grid()

        if settings.get("DEFAULT", "show_errors") == "True":
            yes_butt.select()
            yes_butt.invoke()
        elif settings.get("DEFAULT", "show_errors") == "False":
            no_butt.select()
            no_butt.invoke()
        else:
            tkinter.messagebox.showerror("Error", "Corrupt settings file")
            settings_window.destroy()
            return 1

        timeout_frame = LabelFrame(settings_window,
                                 bg=self.bg_color,
                                 text="Networks",
                                 fg=self.foreground_color)
        timeout_frame.pack(padx=5)

        Label(timeout_frame,
              bg=self.bg_color,
              text="Connection timeout[ms]",
              fg=self.foreground_color).grid(row=0, column=0, sticky=E)

        timeout_spinbox=Spinbox(timeout_frame,
                                activebackground=self.active_butt_color,
                                buttonbackground=self.butt_color,
                                from_=1,
                                to=10000,
                                increment=500)
        timeout_spinbox.grid(row=0, column=1, sticky=W)

        timeout_spinbox.delete(0, END)
        timeout_spinbox.insert(END, settings.get("DEFAULT", "timeout_milliseconds"))

        theme_frame = LabelFrame(settings_window,
                                 bg=self.bg_color,
                                 text="Theme",
                                 fg=self.foreground_color)
        theme_frame.pack(padx=5)

        theme_selector_var=StringVar(theme_frame)
        avalible_themes = theme.sections()
        avalible_themes.pop(0) #removes the "selected" section

        def change_selected_theme(var):
            #clears all the data
            bg_field.delete(0, END)
            alt_bg_field.delete(0, END)
            butt_field.delete(0, END)
            active_butt_field.delete(0, END)
            butt_fg_field.delete(0, END)
            fg_field.delete(0, END)
            theme_name_field.delete(0, END)

            #inserts the new data
            self.selected_theme.set(var)
            bg_field.insert(END, theme.get(self.selected_theme.get(), "background"))
            alt_bg_field.insert(END, theme.get(self.selected_theme.get(), "secondary_background"))
            butt_field.insert(END, theme.get(self.selected_theme.get(), "button_color"))
            active_butt_field.insert(END, theme.get(self.selected_theme.get(), "active_button_color"))
            butt_fg_field.insert(END, theme.get(self.selected_theme.get(), "button_foreground"))
            fg_field.insert(END, theme.get(self.selected_theme.get(), "foreground"))
            theme_name_field.insert(END, self.selected_theme.get())

        theme_selector_var.set(self.selected_theme.get())
        theme_selector=OptionMenu(theme_frame,
                                  theme_selector_var,
                                  *avalible_themes, command=change_selected_theme)
        theme_selector.config(bg=self.butt_color,
                              fg=self.butt_fg_color,
                              activebackground=self.active_butt_color,
                              activeforeground=self.butt_fg_color,
                              highlightthickness=0)
        theme_selector.grid(row=0, column=1, padx=3, pady=2)
        Label(theme_frame,
              bg=self.bg_color,
              text="Selected theme",
              fg=self.foreground_color).grid(row=0, column=0, sticky=E)

        Label(theme_frame,
              bg=self.bg_color,
              text="Background color",
              fg=self.foreground_color).grid(row=1, column=0, sticky=E)
        bg_field = Entry(theme_frame,
                         width=8,
                         exportselection=0,
                         bg="white")
        bg_field.insert(END, self.bg_color)
        bg_field.grid(row=1, column=1, sticky=W, padx=3)

        Label(theme_frame,
              bg=self.bg_color,
              text="Secondary background color",
              fg=self.foreground_color).grid(row=2, column=0, sticky=E)
        alt_bg_field = Entry(theme_frame,
                             width=8,
                             exportselection=0,
                             bg="white")
        alt_bg_field.grid(row=2, column=1, sticky=W, padx=3)
        alt_bg_field.insert(END, self.second_bg_color)

        Label(theme_frame,
              bg=self.bg_color,
              text="Foreground color",
              fg=self.foreground_color).grid(row=3, column=0, sticky=E)
        fg_field = Entry(theme_frame,
                         width=8,
                         exportselection=0,
                         bg="white")
        fg_field.insert(END, self.foreground_color)
        fg_field.grid(row=3, column=1, sticky=W, padx=3)

        Label(theme_frame,
              bg=self.bg_color,
              text="Button color",
              fg=self.foreground_color).grid(row=4, column=0, sticky=E)
        butt_field = Entry(theme_frame,
                           width=8,
                           exportselection=0,
                           bg="white")
        butt_field.insert(END, self.butt_color)
        butt_field.grid(row=4, column=1, sticky=W, padx=3)

        Label(theme_frame,
              bg=self.bg_color,
              text="Active button color",
              fg=self.foreground_color).grid(row=5, column=0, sticky=E)
        active_butt_field = Entry(theme_frame,
                                  width=8,
                                  exportselection=0,
                                  bg="white")
        active_butt_field.insert(END, self.active_butt_color)
        active_butt_field.grid(row=5, column=1, sticky=W, padx=3)

        Label(theme_frame,
              bg=self.bg_color,
              text="Button foreground",
              fg=self.foreground_color).grid(row=6, column=0, sticky=E)
        butt_fg_field = Entry(theme_frame,
                              width=8,
                              exportselection=0,
                              bg="white")
        butt_fg_field.insert(END, self.butt_fg_color)
        butt_fg_field.grid(row=6, column=1, sticky=W, padx=3)

        Label(theme_frame,
              bg=self.bg_color,
              text="Theme name",
              fg=self.foreground_color).grid(row=7, column=0, sticky=E)
        theme_name_field = Entry(theme_frame,
                              width=8,
                              exportselection=0,
                              bg="white")
        theme_name_field.insert(END, self.selected_theme.get())
        theme_name_field.grid(row=7, column=1, sticky=W, padx=3)



        def save():
            if show_errors_var.get() == "Yes":
                settings.set("DEFAULT", "show_errors", "True")
                self.show_errors=True
            else:
                settings.set("DEFAULT", "show_errors", "False")
                self.show_errors=False

            try:
                self.timeout=int(timeout_spinbox.get())
            except:
                timeout_spinbox.delete(0, END)
                return 0
            settings.set("DEFAULT", "timeout_milliseconds", str(self.timeout))

            theme.set(self.selected_theme.get(), "background", bg_field.get())
            theme.set(self.selected_theme.get(), "secondary_background", alt_bg_field.get())
            theme.set(self.selected_theme.get(), "button_color", butt_field.get())
            theme.set(self.selected_theme.get(), "active_button_color", active_butt_field.get())
            theme.set(self.selected_theme.get(), "button_foreground", butt_fg_field.get())
            theme.set(self.selected_theme.get(), "foreground", fg_field.get())
            theme.set("selected", "name", self.selected_theme.get())

            self.bg_color=bg_field.get()
            self.second_bg_color=alt_bg_field.get()
            self.butt_color=butt_field.get()
            self.active_butt_color=active_butt_field.get()
            self.butt_fg_color=butt_fg_field.get()
            self.foreground_color=fg_field.get()

            #this might be implemented later
            '''self.god_window.config(bg=self.bg_color)
            self.toolbar_frame.config(bg=self.second_bg_color)
            self.log_frame.config(bg=self.bg_color)
            self.info_frame.config(bg=self.bg_color)
            self.left_hand_frame.config(bg=self.bg_color)
            self.right_hand_frame.config(bg=self.bg_color)'''

            try:
                with open('theme.ini', 'w') as new_theme:
                    theme.write(new_theme)
                    theme.update()
                    new_theme.close()

                with open('settings.ini', 'w') as new_configfile:
                    settings.write(new_configfile)
                    tkinter.messagebox.showinfo("Saved",
                                                "Saved successfully\nPlease restart dolphin to make changes take full effect")
                    settings.update()
                    new_configfile.close()

                    self.bg_color=bg_field.get()
                    self.second_bg_color=alt_bg_field.get()
                    self.butt_color=butt_field.get()
                    self.active_butt_color=active_butt_field.get()
                    self.butt_fg_color=butt_fg_field.get()
                    self.foreground_color=fg_field.get()

                    settings_window.destroy()
            except:
                tkinter.messagebox.showerror("Error", "Could not save")
                settings_window.destroy()

        def cancel():
            settings_window.destroy()
            return 0

        butt_frame = Frame(settings_window, bg=self.bg_color)
        butt_frame.pack(side=BOTTOM, pady=4)
        connect_butt = Button(butt_frame,
                              text="Save",
                              fg='#86FF59',
                              activeforeground='green',
                              command=save,
                              bg=self.butt_color,
                              activebackground=self.active_butt_color)
        cancel_butt = Button(butt_frame,
                             text="Cancel",
                             fg='#FA4854',
                             activeforeground='red',
                             command=cancel,
                             bg=self.butt_color,
                             activebackground=self.active_butt_color)
        connect_butt.grid(column=0, row=0, padx=5)
        cancel_butt.grid(column=1, row=0)

        settings_window.mainloop()

    def command_interpreter(self, client_message):
        if client_message == "/quit":
            os._exit(0)

        elif client_message == "/dc":
            self.disconnect()

        elif client_message == "/help":
            for command, desc in self.command_dict.items():
                self.print_to_log(command + desc)
            self.s.send(str.encode(client_message))

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
            self.username.set('')
        except OSError as e:
            if self.show_errors:
                self.print_to_log(e)

    def print_to_log(self, msg):
        self.msg_log.insert(END, msg)
        if self.msg_log.size() > 30:
            self.msg_log.yview_scroll(1, UNITS) #scrolls 1 line down

    def read_input(self):
        if self.user_input.get() == '':
            return 0
        try:
            if self.user_input.get()[0:1] == "/":
                self.command_interpreter(self.user_input.get())  # lauches command intepreter
            else:
                self.s.send(str.encode(self.user_input.get()))  # was not a comman

        except OSError:#not connectde to a sever
            self.print_to_log(self.user_input.get())
        except AttributeError:#not connectde to a sever, different depending on platform
            self.print_to_log(self.user_input.get())
        finally:
            self.user_input.set("")

    def manual_connect(self):
        connet_window=Tk()
        connet_window.title("Manual Connect")
        connet_window.configure(bg=self.bg_color)
        #username
        Label(connet_window, text="Username", bg=self.bg_color, fg=self.foreground_color).grid(row=0, column=0, sticky='E')
        username_field=Entry(connet_window,
                         width=16,
                         exportselection=0,
                         textvariable= self.username,
                         bg="white")
        username_field.grid(row=0, column=1, sticky='W', pady=2)

        #ip
        Label(connet_window, text="IP adresss", bg=self.bg_color, fg=self.foreground_color).grid(row=1, column=0, sticky='E')
        chat_server_field=Entry(connet_window,
                              width=16,
                              exportselection=0,
                              textvariable=self.chat_server,
                              bg="white")
        chat_server_field.grid(row=1, column=1, pady=2)

        #port
        Label(connet_window, text="Port", bg=self.bg_color, fg=self.foreground_color).grid(row=2, column=0, sticky='E')
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

        network_protocol_frame=LabelFrame(connet_window, text="Network Protocol", bg=self.bg_color, fg=self.foreground_color)
        network_protocol_frame.grid(row=3, columnspan=2, pady=2)
        ipv4_butt = Radiobutton(network_protocol_frame,
                                text="IPv4", variable=self.network_protocol,
                                value='IPv4',
                                command=setIPv4,
                                bg = self.bg_color,
                                fg=self.foreground_color)
        ipv4_butt.grid()
        ipv4_butt.select()
        ipv6_butt = Radiobutton(network_protocol_frame,
                                text="IPv6",
                                variable=self.network_protocol,
                                value='IPv6',
                                command=setIPv6,
                                bg=self.bg_color,
                                fg=self.foreground_color)
        ipv6_butt.grid()

        #buttons frame
        def cancel():
            self.username.set('')
            self.chat_server.set('')
            self.port.set(0)
            self.network_protocol.set('')
            connet_window.destroy()

        def connect():

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


        butt_frame=Frame(connet_window, bg=self.bg_color)
        butt_frame.grid(row=4, columnspan=2, pady=4)
        connect_butt=Button(butt_frame,
                            text="Connect",
                            fg='#86FF59',
                            activeforeground='green',
                            command=connect,
                            bg=self.butt_color,
                           activebackground=self.active_butt_color)
        cancel_butt=Button(butt_frame,
                           text="Cancel",
                           fg='#FA4854',
                           activeforeground='red',
                           command=cancel,
                           bg=self.butt_color,
                           activebackground=self.active_butt_color)
        connect_butt.pack(side=LEFT, padx=5)
        cancel_butt.pack(side=RIGHT)

        connet_window.mainloop()

    def disconnect(self):
        self.s.shutdown(0)
        self.s.close()
        self.username.set('')
        #self.chat_server.set('') this is done in self.recieve_messages()
        self.port.set(0)
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
            self.s.settimeout(self.timeout)
            self.s.connect((self.chat_server.get(), self.port.get()))
            self.s.settimeout(None)
            self.print_to_log(("Connected to: " + self.chat_server.get()))
            data = self.s.recv(2048)  # recieve the message of the day
            self.print_to_log("Message of the day: " + str(data.decode('utf-8')))  # currently just a random quote
            self.s.send(str.encode(self.username.get()))  # inform the server of your username
            reciever = threading.Thread(target=self.recieve_messages, daemon=0)
            reciever.start()
            self.c_or_dc.set("Disconnect")
        except socket.error as e:  # couldn't connect to given IP + port
            self.print_to_log(("Cound not connect to " + self.chat_server.get() + ":" + str(self.port.get())))
            if self.show_errors:
                self.print_to_log(str(e))

    def build_window(self, window):
        window.title("Dolphin")

        #Q:why are all the frames "self."?
        #A:it is a legacy that does not really need to be removed but is serves no purpose
        #that is also the case with the self.god_window frame
        self.god_window=Frame(window, bg=self.second_bg_color)
        self.god_window.pack()
        self.toolbar_frame = Frame(self.god_window, bg=self.second_bg_color)  # the toolbar frame
        self.toolbar_frame.pack(side=TOP, fill=X)

        self.right_hand_frame = Frame(self.god_window, bg=self.bg_color)  # splits the rest of the window in two
        self.right_hand_frame.pack(side=RIGHT, fill=Y)
        self.left_hand_frame = Frame(self.god_window, bg=self.bg_color)
        self.left_hand_frame.pack(side=LEFT, fill=Y)

        self.info_frame = LabelFrame(self.right_hand_frame,  # creates the info frame
                                text="Connection information",
                                bg=self.bg_color,
                                fg=self.foreground_color)
        self.info_frame.pack(pady=5, padx=5)

        ad_frame = Frame(self.right_hand_frame, bg="black")  # the advertisment frame (optinal)
        ad_frame.pack(side=BOTTOM)
        self.entry_frame = Frame(self.left_hand_frame, bg=self.bg_color)
        self.entry_frame.pack(side=BOTTOM, fill=X)  # user input frame

        self.log_frame = Frame(self.left_hand_frame, bg=self.bg_color)  # the log and log scroll frame
        self.log_frame.pack(side=LEFT, fill=Y)
        #the following objects actuallly need to have the "self." part

        #Label(self.entry_frame, text=">>>", bg=self.bg_color, fg=self.foreground_color).pack(side=RIGHT)  # the 3 arrows
        Button(self.entry_frame,
               text=" Send ",
               bg=self.butt_color,
               activebackground=self.active_butt_color,
               fg=self.butt_fg_color,
               command=self.read_input).pack(side=RIGHT)

        scroll = Scrollbar(self.log_frame, orient=VERTICAL)  # scroller
        scroll.pack(side=RIGHT, fill=Y, pady=5)

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
                               yscrollcommand=scroll.set)  # text thing
        self.msg_log.pack(padx=5, pady=5, side=LEFT)
        scroll['command'] = self.msg_log.yview

        self.user_input = StringVar()
        entry = Entry(self.entry_frame,  # the input field
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

        info_keys = [Label(self.info_frame, text="Server name:", bg=self.bg_color, fg=self.foreground_color),
                          Label(self.info_frame, text="IP:", bg=self.bg_color, fg=self.foreground_color),
                          Label(self.info_frame, text="Username:", bg=self.bg_color, fg=self.foreground_color),
                          Label(self.info_frame, text="Level:", bg=self.bg_color, fg=self.foreground_color)]

        info_values = [Label(self.info_frame, text="placeholder", bg=self.bg_color, fg=self.foreground_color),
                            Label(self.info_frame, textvariable=self.chat_server, bg=self.bg_color, fg=self.foreground_color),
                            Label(self.info_frame, textvariable=self.username, bg=self.bg_color, fg=self.foreground_color),
                            Label(self.info_frame, text="placeholder", bg=self.bg_color, fg=self.foreground_color)]

        for n in range(len(info_keys)):
            info_keys[n].grid(row=n, column=0, sticky=E)
            info_values[n].grid(row=n, column=1, sticky=W)

        ad = Label(ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5, font="Impact")
        ad.pack(padx=5, pady=5)

        # TOOLBAR BUTTONS

        def conn_or_disconn():
            if self.c_or_dc.get() == "Connect":
                for thread in threading.enumerate():
                    if str(thread)[0:15] == "<Thread(connect":
                        return 0
                manual_conn_thread = threading.Thread(target=self.manual_connect, daemon=1, name="connect")
                manual_conn_thread.start()
            elif self.c_or_dc.get() == "Disconnect":
                self.disconnect()

        self.c_or_dc = StringVar()
        self.c_or_dc.set("Connect")
        connect_butt = Button(self.toolbar_frame,
                              textvariable=self.c_or_dc,
                              command=conn_or_disconn,
                              bg=self.butt_color,
                              bd=2,
                              height=2,
                              fg=self.butt_fg_color,
                              activebackground=self.active_butt_color)

        self.profile_butt = Menubutton(self.toolbar_frame,
                                       text="Profiles",
                                       relief=RAISED,
                                       bd=2,
                                       height=2,
                                       bg=self.butt_color,
                                       fg=self.butt_fg_color,
                                       activebackground=self.active_butt_color)
        self.profile_butt.menu=Menu(self.profile_butt,
                                    bd=2,
                                    tearoff=0,
                                    bg=self.butt_color,
                                    fg=self.butt_fg_color,
                                    activebackground=self.active_butt_color)

        def new_profile():
            #by starting this in a new thread you will be able to recive messages while creating profiles
            for thread in threading.enumerate():
                if str(thread)[0:19]=="<Thread(new_profile":
                    return 0
            new_profile_thread = threading.Thread(target=self.new_profile, daemon=1, name="new_profile")
            new_profile_thread.start()

        def edit_profile():
            for thread in threading.enumerate():
                if str(thread)[0:20]=="<Thread(edit_profile":
                    return 0
            edit_profile_thread = threading.Thread(target=self.edit_profiles, daemon=1, name="edit_profile")
            edit_profile_thread.start()

        def settings():
            for thread in threading.enumerate():
                if str(thread)[0:16]=="<Thread(settings":
                    return 0
            settings_thread = threading.Thread(target=self.settings, daemon=1, name="settings")
            settings_thread.start()

        self.profile_butt['menu']=self.profile_butt.menu
        self.profile_butt.menu.add_command(label='New', command=new_profile)
        self.profile_butt.menu.add_command(label='Edit', command=edit_profile)
        self.profile_butt.menu.add_separator()

        #adds the pre-existing profiles
        profiles = configparser.ConfigParser()
        profiles.read("profiles.ini")
        
        for label in profiles.sections():
            self.add_profile_to_butt_cascade(label)
        #done adding the pre-existing profiles

        settings_butt = Button(self.toolbar_frame,
                               text="Settings",
                               height=2,
                               bd=2,
                               bg=self.butt_color,
                               fg=self.butt_fg_color,
                               activebackground=self.active_butt_color,
                               command=settings)

        connect_butt.pack(side=LEFT, padx=3, pady=2)
        self.profile_butt.pack(side=LEFT, padx=3, pady=2)
        settings_butt.pack(side=LEFT, padx=3, pady=2)

    def remove_profile_from_butt_cascade(self, label):
        menu_index=3
        for n in range(len(self.profile_button_selections)):
            try:
                if self.profile_button_selections[n].label == label:
                    self.profile_butt.menu.delete(menu_index)
                    self.profile_button_selections[n]=None
                    break
                else:
                    #objektet hade attributet label men det var inte rätt
                    menu_index +=1
            except AttributeError:
                pass
                #objektet var None och har därför tagigts bort
                #detta innebär att alla element "under" (grafiskt) i menyn har flyttats ett steg upp(grafiskt) eller ett steg ner i dess index
                #för att kompensera för detta så ökar INTE menu_index.

    def add_profile_to_butt_cascade(self, label):
        n=len(self.profile_button_selections)
        self.profile_button_selections.append(ProfileButtons(n, label))
        self.profile_butt.menu.add_command(label=label, command=self.profile_button_selections[n].call)

    def __init__(self, window):
        self.chat_server = StringVar()
        self.port = IntVar()
        self.username = StringVar()
        self.network_protocol = StringVar()
        self.profile_button_selections=[]

        try:
            theme = configparser.ConfigParser()
            theme.read("theme.ini")

            self.selected_theme = StringVar()
            self.selected_theme.set(theme.get("selected", "name"))

            self.bg_color = theme.get(self.selected_theme.get(), "background")
            self.second_bg_color = theme.get(self.selected_theme.get(), "secondary_background")
            self.butt_color = theme.get(self.selected_theme.get(), "button_color")
            self.active_butt_color = theme.get(self.selected_theme.get(), "active_button_color")  # color when mouse hovers over it/clicks it
            self.butt_fg_color = theme.get(self.selected_theme.get(), "button_foreground")
            self.foreground_color = theme.get(self.selected_theme.get(), "foreground")
            # self.font = font.Font(family=theme.get(self.selected_theme.get(), "font"), size=10) this is also a legacy
        except:
            tkinter.messagebox.showerror("Error", "Corrupt theme file")
        try:
            settings_file = configparser.ConfigParser()
            settings_file.read("settings.ini")

            if settings_file.get("DEFAULT", "show_errors") == "True":
                self.show_errors = True
            elif settings_file.get("DEFAULT", "show_errors") == "False":
                self.show_errors = False
            else:
                raise configparser.NoOptionError  # not quite the right error but hey

            self.timeout= settings_file.getint("DEFAULT", "timeout_milliseconds")/1000 # det skall vara i millisekunder
        except:
            tkinter.messagebox.showerror("Error", "Corrupt settings file")

        self.command_dict = {"/help": self.spacer(20, "/help") + "view this page",
                        "/quit": self.spacer(20, "/quit") + "exit program",
                             "/dc": self.spacer(20, "/dc") + "disconnect from server"}

        self.build_window(window)
        self.print_to_log(version)

window = Tk()  # creates the main window

gui_obj = GUI(window)
window.mainloop()
import tkinter.messagebox
from tkinter import *
window = Tk() #creates the main window
window.title("Dolphin")

def print_to_log(msg):
    msg_log.insert(END, msg)
    if msg_log.size() > 30:
        msg_log.yview_scroll(1, UNITS)

def read_input(event):  # that bitch .bind() wannts to pass the event(the key press) so i have to take it
    if user_input.get() == '':
        return 0
    print_to_log(user_input.get())
    user_input.set("")

toolbar_frame=Frame(window, bg="grey")#the toolbar frame
toolbar_frame.pack(side=TOP, fill=X)

right_hand_frame=Frame(window) # splits the rest of the window in two
right_hand_frame.pack(side=RIGHT, fill=Y)
left_hand_frame=Frame(window, bg="blue")
left_hand_frame.pack(side=LEFT, fill=Y)

info_frame = LabelFrame(right_hand_frame, #creates the info frame
                        text="Connection information",
                        fg="black")
info_frame.pack(pady=5, padx=5)

ad_frame =Frame(right_hand_frame, bg="black") #the advertisment frame (optinal)
ad_frame.pack(side=BOTTOM)
entry_frame = Frame(left_hand_frame)
entry_frame.pack(side=BOTTOM, fill=X) #user input frame

log_frame = Frame(left_hand_frame) #the log and log scroll frame
log_frame.pack(side=LEFT, fill=Y)

entry_marking=Label(entry_frame, text=">>>") #the 3 arrows
entry_marking.pack(side=LEFT)

scroll = Scrollbar(log_frame, orient=VERTICAL) #scroller
scroll.pack(side=RIGHT, fill=Y, pady=5)

log= StringVar() #holds the data for the log widow
msg_log=Listbox(log_frame, #the logframe
                height=30, width=100,
                bg="white",
                selectbackground="white",
                selectforeground="black",
                selectmode=SINGLE,
                activestyle=NONE,
                listvariable=log,
                exportselection=0,
                highlightbackground="grey",
                yscrollcommand=scroll.set) #text thing
msg_log.pack(padx=5, pady=5, side=LEFT)
scroll['command']=msg_log.yview

user_input=StringVar()
entry=Entry(entry_frame, #the actual input field
            width=95,
            highlightbackground="blue",
            bg="white",
            exportselection = 0)
entry.textvariable=user_input

entry.bind('<Return>', read_input) #makes enter key send message
entry.pack(padx=5, pady=5, side=LEFT)

info_keys_color="#595959"
info_keys=[Label(info_frame, text="Server name:", fg=info_keys_color),
           Label(info_frame, text="IP:", fg=info_keys_color)]

info_values=[Label(info_frame, text="Pewds h8 club", fg=info_keys_color),
             Label(info_frame, text="127.0.0.1", fg=info_keys_color)]

ad=Label(ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5)
ad.pack(padx=5, pady=5)

for n in range(len(info_keys)):
    info_keys[n].grid(row=n, column=0, sticky=E)
    info_values[n].grid(row=n, column=1, sticky=W)

#TOOLBAR BUTTONS
profile_butt = Button(toolbar_frame,text="Profiles")
settings_butt = Button(toolbar_frame, text="Settings")
change_butt = Button(toolbar_frame, text="Change Server")
diconn_butt = Button(toolbar_frame, text="Disconnect")

profile_butt.pack(side=LEFT, padx=3, pady=2)
settings_butt.pack(side=LEFT, padx=3, pady=2)
change_butt.pack(side=LEFT, padx=3, pady=2)
diconn_butt.pack(side=LEFT, padx=3, pady=2)


window.mainloop()
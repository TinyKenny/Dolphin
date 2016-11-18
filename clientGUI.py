import tkinter.messagebox
from tkinter import *

window = Tk()
window.title("Dolphin")

#parents: window
toolbar_frame=Frame(window, bg="grey")
toolbar_frame.pack(side=TOP, fill=X)

right_hand_frame=Frame(window, bg="yellow")
right_hand_frame.pack(side=RIGHT, fill=Y)

left_hand_frame=Frame(window, bg="blue")
left_hand_frame.pack(side=LEFT, fill=Y)


info_frame = Frame(right_hand_frame, bg="grey", bd=2)
info_frame.pack(pady=5)

ad_frame =Frame(right_hand_frame, bg="black")
ad_frame.pack(side=BOTTOM)

log_frame = Frame(left_hand_frame, bg="pink")
log_frame.pack(side=TOP)

entry_frame = Frame(left_hand_frame, bg="green")
entry_frame.pack(side=BOTTOM, fill=Y)#entry frame

entry_marking=Label(entry_frame, text=">>>")
entry_marking.pack(side=LEFT)

text_thing=Text(log_frame, wrap=WORD, highlightbackground="black", bg="white") #text thing
text_thing.pack(padx=5)

entry=Entry(entry_frame, width=66, highlightbackground="black", bg="white")#entry field
entry.pack(padx=5, pady=5, side=LEFT)

#scroll=Scrollbar(log_frame)
#scroll.config(command=text_thing.yview)
#scroll.pack(side=RIGHT, fill=Y, padx=0, pady=5)

color="grey"
info_keys=[Label(info_frame, text="Server name:", bg=color),
           Label(info_frame, text="IP:", bg=color)]

info_values=[Label(info_frame, text="Pewds h8 club", bg=color),
             Label(info_frame, text="127.0.0.1", bg=color)]

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

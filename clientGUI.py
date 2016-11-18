import tkinter.messagebox
from tkinter import *

window = Tk()
window.title("Dolphin")

#parents: window
toolbar_frame=Frame(window, bg="grey")
right_hand_frame=Frame(window)
left_hand_frame=Frame(window)

#parents: window, left_hand_frame
log_frame = Frame(left_hand_frame)
entry_frame = Frame(left_hand_frame)
info_frame = Frame(right_hand_frame, bg="lightgrey", bd=0)
ad_frame =Frame(right_hand_frame, bg="black")

entry=Entry(entry_frame)
entry_marking=Label(entry_frame, text=">>>")
text_thing=Text(log_frame)

color="lightgrey"
info_keys=[Label(info_frame, text="Server name:", bg=color),
           Label(info_frame, text="IP:", bg=color)]

info_values=[Label(info_frame, text="Pewds h8 club", bg=color),
             Label(info_frame, text="127.0.0.1", bg=color)]

ad=Label(ad_frame, text="csgogambling.com", relief=GROOVE, fg="yellow", bg="red", bd=1, height=5)

toolbar_frame.pack(side=TOP, fill=X)
right_hand_frame.pack(side=RIGHT, fill=Y)
left_hand_frame.pack(side=LEFT, fill=Y)

info_frame.pack(fill=Y, pady=5, padx=5)
entry_marking.pack(side=LEFT)
entry_frame.pack(side=BOTTOM, fill=X)
log_frame.pack(side=LEFT, fill=Y)
ad_frame.pack(side=BOTTOM)

entry.pack(padx=5, pady=5, fill=X)
for n in range(len(info_keys)):
    info_keys[n].grid(row=n, column=0, sticky=E)
    info_values[n].grid(row=n, column=1, sticky=W)

text_thing.pack(padx=5, pady=5)
ad.pack(padx=5, pady=5)

profile_butt = Button(toolbar_frame,text="Profiles")
settings_butt = Button(toolbar_frame, text="Settings")
change_butt = Button(toolbar_frame, text="Change Server")
diconn_butt = Button(toolbar_frame, text="Disconnect")

profile_butt.pack(side=LEFT, padx=3, pady=2)
settings_butt.pack(side=LEFT, padx=3, pady=2)
change_butt.pack(side=LEFT, padx=3, pady=2)
diconn_butt.pack(side=LEFT, padx=3, pady=2)

window.mainloop()

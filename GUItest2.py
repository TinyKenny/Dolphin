import tkinter.messagebox
from tkinter import *

window = Tk()
window.title("Dolphin")
toolbar_frame=Frame(window, bg="grey")
outside_else_frame=Frame(window)
toolbar_frame.pack(side=TOP, fill=X)
outside_else_frame.pack(side=BOTTOM)
else_frame=Frame(outside_else_frame)
else_frame.grid()

for n in range(4):
    else_frame.rowconfigure(n)
for n in range(4):
    else_frame.columnconfigure(n)

log_frame = Frame(else_frame, bg="blue")
info_frame = Frame(else_frame, bg="red")
ad_frame =Frame(else_frame, bg="green")

log_frame.grid(row=0, column=0, rowspan=2)
info_frame.grid(row=0, column=1)
ad_frame.grid(row=1, column=1)

text_thing=Text(log_frame)
text_thing.pack(padx=5, pady=5)

text_thing1=Label(info_frame, text="Server: pewd h8 club\nConneced to 79.134.23.34")
text_thing1.pack(padx=5, pady=5)
text_thing1=Label(ad_frame, text="csgogambling.com")
text_thing1.pack(padx=5, pady=5)

profile_butt = Button(toolbar_frame,text="Profiles")
settings_butt = Button(toolbar_frame, text="Settings")
change_butt = Button(toolbar_frame, text="Change Server")
diconn_butt = Button(toolbar_frame, text="Disconnect")

profile_butt.pack(side=LEFT, padx=3, pady=2)
settings_butt.pack(side=LEFT, padx=3, pady=2)
change_butt.pack(side=LEFT, padx=3, pady=2)
diconn_butt.pack(side=LEFT, padx=3, pady=2)

window.mainloop()

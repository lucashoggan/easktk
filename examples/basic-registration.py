from tkinter import Label, Entry, Button, StringVar, Tk
from easytk import ETKWindow

win = ETKWindow(Tk())

def register_subwindow():
    sub = win.sub()
    sub.m.geometry("300x95")
    sub.state.add("email", StringVar())
    sub.state.add("password", StringVar())
    sub.widgets.add("email-in", Entry(sub.m, textvariable=sub.state.get("email"), width=35))
    sub.widgets.ent_placeholder("email-in", "email")
    sub.widgets.last.pack()
    sub.widgets.add("password-in", Entry(sub.m, textvariable=sub.state.get("password"), show="*"))
    sub.widgets.ent_placeholder("password-in", "password")
    sub.widgets.last.pack()
    def on_submit():
        print("Email:", sub.state.val("email"))
        print("Password:", sub.state.val("password"))
        sub.m.destroy()
        
    
    sub.widgets.add("btn-1", Button(sub.m, text="submit", command=on_submit))
    sub.widgets.get("btn-1").pack()
    
win.m.geometry("150x40+250+250")
win.widgets.add("reg-btn", Button(win.m, text="Register", command=register_subwindow))
win.widgets.last.pack()

win.run()

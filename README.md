# EasyTk
A python package to make working in tkinter even easier, hope to add docs soon.

## Usage
### Download
```bash 
curl https://rawcdn.githack.com/lucashoggan/easytk/d0dbd6fede91c5f121bd8cdbde16933811bbf8bd/easytk.py -o easytk.py
# or
wget https://rawcdn.githack.com/lucashoggan/easytk/d0dbd6fede91c5f121bd8cdbde16933811bbf8bd/easytk.py
# or
git clone https://github.com/lucashoggan/easytk
mv easytk/easytk.py ./easytk.py
rm -rf easytk
```
### Importing package and window setup
```python
# import package
from easytk import ETKWindow
from tkinter import Tk

# setup window
win = ETKWindow(Tk())
# run window
win.run()
```
### Widgets
```python
# add widget
from tkinter import Label # uses native tkinter widgets at the moment

# if no master is provided for widget, widget will bind to first initalised 
# ETKWindow class, so for subwindows the master must be provided
win.widgets.add("lbl-1", Label(text="Hello World")) # no master provided
win.widgets.add("lbl-1", Label(win.master, text="Hello World")) # master (longhand)
# there is a shorthand for the master varible to make providing it quicker
win.widgets.add("lbl-1", Label(win.m, text="Hello world"))

# get widget
win.widgets.get("lbl-1")
# OR
win.widgets["lbl-1"]
# OR to get the last added widget
win.widgets.last

# example: placing widget
win.widgets["lbl-1"].place(x=10, y=10)
win.widgets.last.place(x=10, y=10)
```
#### Adding a placeholder to entry widget
- This adds a placeholder that disapears when the user selects or types in the entry box
```python 
win.widgets.add("email-entry", Entry(win.m, text="email"))
win.widgets.ent_placeholder("email-entry", "email")
```
#### Using "after-funcs"
- These are functions performed onto the widget in the add function to make setup even easier, can do things such as place an object in the same line its added such as below
- they're setup so you can add as many functions as you like
```python
win.widgets.add("heading", Label(win.m, text="Hello"), lambda win: win.pack())
# Multible actions
win.widgets.add("btn", Button(win.m, text="Submit"), lambda w: w.pack(), lambda w: w.config(text="Submit!"))
```
### Background Processes
- Use these to stop other processing getting in the way of the drawing gui e.g data fetching, these functions will run indefinetly until destroyed.
```python
# add process
@win.processes.add("api-call", auto_start_process=False)
def api_call()
    # ...call API

    # IMPORTANT: use ETKWindow.queue.add when updating the gui in any way from a background process
    # otherwise, thread errors will occur
    win.queue.add(lambda: win.widgets["lbl-1"].config(text=API_RETURN))

# OR
win.processes.add_f("api-call", api_call)

# Start process
win.processes.start("api-call")
# OR set the auto_start_process flag to TRUE to start right after definition

# End process
win.processes.destroy("api-call")
```

### State
```python
# add state
win.state.add("txt-in-1", "")

# bind state to text input
win.widgets.add("txt-in", Entry())
win.widgets.bind_state("txt-in", win.state["txt-in-1"])

# get value of state
win.state["txt-in-1"].v

# set value of state
win.state["txt-in-1"].v = "Hello"
```
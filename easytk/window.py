from easytk.processes import ETKQueueManager, ETKBackgroundProcessManager
from easytk.widgets import ETKWidgetManager
from easytk.state import ETKStateManager
from tkinter import Tk, Toplevel


class ETKWindow:
    widgets: ETKWidgetManager
    state: ETKStateManager
    processes: ETKBackgroundProcessManager
    queue: ETKQueueManager
    master: Tk | Toplevel
    def __init__(self, master: Tk|Toplevel):
        self.master = master
        self.widgets = ETKWidgetManager()
        self.state = ETKStateManager(self.master)
        self.processes = ETKBackgroundProcessManager()
        self.queue = ETKQueueManager(self.master)
    
    def sub(self): return ETKWindow(Toplevel(self.master))
    
    @property
    def m(self): return self.master    
        
    def run(self): 
        self.master.mainloop()
        self.processes.destroy_all()
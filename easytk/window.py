from easytk.processes import ETKQueueManager, ETKBackgroundProcessManager
from easytk.widgets import ETKWidgetManager, ETKFrameManager
from easytk.state import ETKStateManager
from tkinter import Tk, Toplevel


class ETKWindow:
    widgets: ETKWidgetManager
    state: ETKStateManager
    processes: ETKBackgroundProcessManager
    queue: ETKQueueManager
    frames: ETKFrameManager
    master: Tk | Toplevel
    def __init__(self, master: Tk|Toplevel):
        self.master = master
        self.widgets = ETKWidgetManager()
        self.state = ETKStateManager(self.master)
        self.processes = ETKBackgroundProcessManager()
        self.queue = ETKQueueManager(self.master)
        self.frames = ETKFrameManager()
    
    
    def sub(self): return ETKWindow(Toplevel(self.master))
    
    @property
    def m(self): return self.master    
        
    def geometry(self, geometry_string: str):
        """Set the window geometry (size and position).
        
        Args:
            geometry_string (str): Geometry string in format 'widthxheight+x+y' or 'widthxheight'
        """
        self.master.geometry(geometry_string)
        return self
    
    def title(self, title: str):
        """Set the window title.
        
        Args:
            title (str): The title to set for the window
        """
        self.master.title(title)
        return self
        
    def run(self): 
        self.master.mainloop()
        self.processes.destroy_all()

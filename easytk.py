from typing import Any, Dict, cast, Callable, Optional
from tkinter import StringVar, Tk, Widget, IntVar
from queue import Queue, Empty as q_Empty
from threading import Thread, Event

class ETKWidgetManager:
    widgets: Dict[str, Widget]
    master: Tk
    def __init__(self, master:Tk):
        self.widgets = {}
        self.master = master
    
    def add(self, name:str, wid:Widget):
        if name not in self.widgets:
            wid.master = self.master
            self.widgets[name] = wid
    
    def get(self, name:str) -> Widget | None:
        if name in self.widgets:
            return self.widgets[name]
        return None
    
    def __getitem__(self, key:str) -> Widget:
        if key in self.widgets: return self.widgets[key]
        raise KeyError

class ETKStateManager:
    state: Dict[str, StringVar | IntVar]
    def __init__(self):
        self.state = {}
    def add(self, name:str, var: (StringVar | IntVar)):
        if name not in self.state:
            self.state[name] = var
            return 
        raise Exception(f"State with name \"{name}\" already exists")
    def get(self, name:str) -> StringVar | IntVar : return self.state[name]
    def val(self, name:str): return self.state[name].get()
    def set(self, name:str, val:str|int):
        if isinstance(self.state[name], StringVar) and isinstance(val, str):
            tmp = cast(StringVar, self.state[name])
            tmp.set(val)
        elif isinstance(self.state[name], IntVar) and isinstance(val, int):
            tmp = cast(IntVar, self.state[name])
            tmp.set(val)
        else:
            raise ValueError(f"Incompatible types between {self.state[name].__class__.__name__} and {val.__class__.__name__}")
            
         
    
    def __getitem__(self, key:str) -> (StringVar | IntVar):
        if key in self.state: return self.state[key]
        raise KeyError     

class ETKBackgroundProcess(Thread):
    e: Event
    def __init__(self, t:Callable[[], None], *args, **kwargs):
        self.e = Event()
        super().__init__(target=self.wrapped_func(t), *args, **kwargs)
  
          
    def wrapped_func(self, t:Callable[[], None]):
        def w(): 
            while not self.e.is_set(): 
                print("Hello", self.e)
                t()
        return w

class ETKQueueManager:
    q: Queue
    start_time: int
    polling_time: int
    def __init__(self, master:Tk, start_time:int=50, polling_time:int=50):
        self.q = Queue()
        self.start_time = start_time
        self.polling_time = polling_time
        self.start_processing(master)
    def process(self, master:Tk):
        try:
            while True:
                func = self.q.get_nowait()
                func()
        except q_Empty:
            pass
        master.after(self.polling_time, lambda: self.process(master))
    def start_processing(self, master:Tk):
        master.after(self.start_time, lambda: self.process(master))
    def add(self, func: Callable[[], None]):
        self.q.put(func)
        
        
        

class ETKBackgroundProcessManager:
    threads: Dict[str, ETKBackgroundProcess]
    master: Tk
    def __init__(self, master:Tk):
        self.threads = {}
        self.master = master
        
    
    def add_f(self, process_name:str, function:Callable[[], Any], auto_start_process:bool=False, allow_process_override:bool=False) -> None:
        if process_name not in self.threads or allow_process_override:
            self.threads[process_name] = ETKBackgroundProcess(t=function)
            if auto_start_process: self.threads[process_name].start()
            return
        raise KeyError(f"Process with name \"{process_name}\" already exists \nIf you want to overide previous process set allow_process_overide=True")
    
    def add(self, process_name:str, auto_start:bool=False, allow_process_override:bool=False):
        def inner(func:Callable[[], None]):
            self.add_f(process_name, func, auto_start, allow_process_override)            
        return inner
            
    
    def start(self, process_name:str):
        self.threads[process_name].start()
    def destroy(self, process_name:str):
        self.threads[process_name].e.set()
    def destroy_all(self):
        for v in self.threads.values():
            v.e.set()

class ETKWindow:
    widgets: ETKWidgetManager
    state: ETKStateManager
    processes: ETKBackgroundProcessManager
    queue: ETKQueueManager
    master: Tk
    def __init__(self):
        self.master = Tk()
        self.widgets = ETKWidgetManager(self.master)
        self.state = ETKStateManager()
        self.processes = ETKBackgroundProcessManager(self.master)
        self.queue = ETKQueueManager(self.master)
        
    def schedule(self, func:Callable[[], None], delay:int=0): self.master.after(delay, func)
        
    def run(self): 
        self.master.mainloop()
        self.processes.destroy_all()
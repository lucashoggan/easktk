from tkinter import StringVar, Tk, Widget, IntVar, Label, Entry, Button, Toplevel
from typing import Any, Dict, cast, Callable, Optional, TypeVar, Generic
from queue import Queue, Empty as q_Empty
from threading import Thread, Event


class ETKWidgetManager:
    widgets: Dict[str, (Label | Entry | Button | Widget)]
    _last_add:str
    def __init__(self):
        self.widgets = {}
        self._last_add = ""
    
    def add(self, name:str, wid:Widget):
        if name not in self.widgets:
            self._last_add = name
            self.widgets[name] = wid
    
    def get(self, name:str) -> Widget: 
        return self.widgets[name]
    @property
    def last(self) -> Widget: 
        if self._last_add != "":
            return self.widgets[self._last_add]
        else:
            raise Exception("ERR - No widgets have been added yet!")
    
    def __getitem__(self, key:str) -> Widget:
        if key in self.widgets: return self.widgets[key]
        raise KeyError
    
    def ent_placeholder(self, ent_name:str, placeholder_txt:str, txt_clr:str="black", placeholder_clr:str="grey", show_important:bool=False): # type: ignore
        if ent_name in self.widgets:
            if isinstance((entry:=self.widgets[ent_name]), Entry):
                entry = cast(Entry, entry)
                show = "" if ((tmp := entry.config()) == None) or show_important else tmp["show"][4] 
                def on_focus(event):
                    if entry.get() == placeholder_txt:
                        entry.delete(0, "end")
                        entry.config(fg=txt_clr)
                        if show != "": entry.config(show=show)
                def on_unfocus(event):
                    if not entry.get():
                        entry.insert(0, placeholder_txt)
                        entry.config(fg=placeholder_clr)
                        if show != "": entry.config(show="")
                on_unfocus(None)
                entry.bind("<FocusIn>", on_focus)
                entry.bind("<FocusOut>", on_unfocus)
            else:
                raise Exception(f"ERR - entry was of type \"{entry.__class__.__name__}\" when it should of been {Entry.__class__.__name__}")
        else:
            raise Exception(f"ERR - No widget with name {ent_name}")


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
                t()
        return w

class ETKQueueManager:
    q: Queue
    start_time: int
    polling_time: int
    def __init__(self, master: Tk|Toplevel, start_time:int=50, polling_time:int=50):
        self.q = Queue()
        self.start_time = start_time
        self.polling_time = polling_time
        self.start_processing(master)
    def process(self, master:Tk|Toplevel):
        try:
            while True:
                func = self.q.get_nowait()
                func()
        except q_Empty:
            pass
        master.after(self.polling_time, lambda: self.process(master))
    def start_processing(self, master:Tk | Toplevel):
        master.after(self.start_time, lambda: self.process(master))
    def add(self, func: Callable[[], None]):
        self.q.put(func)
        
        
        

class ETKBackgroundProcessManager:
    threads: Dict[str, ETKBackgroundProcess]
    def __init__(self):
        self.threads = {}
        
    
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
    master: Tk | Toplevel
    def __init__(self, master: Tk|Toplevel):
        self.master = master
        self.widgets = ETKWidgetManager()
        self.state = ETKStateManager()
        self.processes = ETKBackgroundProcessManager()
        self.queue = ETKQueueManager(self.master)
    
    def sub(self): return ETKWindow(Toplevel(self.master))
    
    @property
    def m(self): return self.master    
        
    def run(self): 
        self.master.mainloop()
        self.processes.destroy_all()
        



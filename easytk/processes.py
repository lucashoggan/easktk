from queue import Queue, Empty as q_Empty
from threading import Thread, Event
from typing import Callable, Dict
from tkinter import Tk, Toplevel

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
        
    
    def add_f(self, process_name:str, function:Callable[[], None], auto_start_process:bool=False, allow_process_override:bool=False) -> None:
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
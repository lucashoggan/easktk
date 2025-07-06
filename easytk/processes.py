from queue import Queue, Empty as q_Empty
from threading import Thread, Event
from typing import Callable, Dict
from tkinter import Tk, Toplevel

class ETKBackgroundProcess(Thread):
    """A background thread that runs a function repeatedly until stopped.
    
    This class wraps a function to run continuously in a separate thread,
    with the ability to cleanly stop execution using an Event.
    """
    e: Event
    def __init__(self, t:Callable[[], None], *args, **kwargs):
        """Initialize the background process.
        
        Args:
            t (Callable[[], None]): The function to run repeatedly in the background
            *args: Additional arguments passed to Thread constructor
            **kwargs: Additional keyword arguments passed to Thread constructor
        """
        self.e = Event()
        super().__init__(target=self.wrapped_func(t), *args, **kwargs)
  
          
    def wrapped_func(self, t:Callable[[], None]):
        """Wraps a function to run repeatedly until the Event is set.
        
        Args:
            t (Callable[[], None]): The function to wrap
            
        Returns:
            Callable[[], None]: A wrapper function that runs t in a loop
        """
        def w(): 
            while not self.e.is_set():
                t()
        return w

class ETKQueueManager:
    """Manages a thread-safe queue for executing functions in the main GUI thread.
    
    This class provides a way for background threads to safely update GUI components
    by queuing functions to be executed in the main thread.
    """
    q: Queue
    start_time: int
    polling_time: int
    def __init__(self, master: Tk|Toplevel, start_time:int=50, polling_time:int=50):
        """Initialize the queue manager.
        
        Args:
            master (Tk | Toplevel): The tkinter window to bind the processing to
            start_time (int, optional): Delay before starting queue processing (ms). Defaults to 50.
            polling_time (int, optional): Interval between queue checks (ms). Defaults to 50.
        """
        self.q = Queue()
        self.start_time = start_time
        self.polling_time = polling_time
        self.start_processing(master)
    def process(self, master:Tk|Toplevel):
        """Process all queued functions and schedule the next processing cycle.
        
        Args:
            master (Tk | Toplevel): The tkinter window to schedule the next processing on
        """
        try:
            while True:
                func = self.q.get_nowait()
                func()
        except q_Empty:
            pass
        master.after(self.polling_time, lambda: self.process(master))
    def start_processing(self, master:Tk | Toplevel):
        """Start the queue processing after the initial delay.
        
        Args:
            master (Tk | Toplevel): The tkinter window to schedule processing on
        """
        master.after(self.start_time, lambda: self.process(master))
    def add(self, func: Callable[[], None]):
        """Add a function to the queue to be executed in the main thread.
        
        Args:
            func (Callable[[], None]): Function to execute in the main GUI thread
        """
        self.q.put(func)
        
        
        

class ETKBackgroundProcessManager:
    """Manages multiple background processes for an ETKWindow.
    
    This class provides methods to create, start, stop, and manage multiple
    background threads that can run continuously alongside the GUI.
    """
    threads: Dict[str, ETKBackgroundProcess]
    def __init__(self):
        """Initialize the background process manager with an empty thread dictionary."""
        self.threads = {}
        
    
    def add_f(self, process_name:str, function:Callable[[], None], auto_start_process:bool=False, allow_process_override:bool=False) -> None:
        """Add a background process using a function directly.
        
        Args:
            process_name (str): Unique name to identify the process
            function (Callable[[], None]): Function to run repeatedly in background
            auto_start_process (bool, optional): Start the process immediately. Defaults to False.
            allow_process_override (bool, optional): Allow overriding existing process with same name. Defaults to False.
            
        Raises:
            KeyError: If process_name already exists and allow_process_override is False
        """
        if process_name not in self.threads or allow_process_override:
            self.threads[process_name] = ETKBackgroundProcess(t=function)
            if auto_start_process: self.threads[process_name].start()
            return
        raise KeyError(f"Process with name \"{process_name}\" already exists \nIf you want to overide previous process set allow_process_overide=True")
    
    def add(self, process_name:str, auto_start:bool=False, allow_process_override:bool=False):
        """Decorator to add a background process.
        
        Args:
            process_name (str): Unique name to identify the process
            auto_start (bool, optional): Start the process immediately. Defaults to False.
            allow_process_override (bool, optional): Allow overriding existing process with same name. Defaults to False.
            
        Returns:
            Callable: Decorator function that registers the decorated function as a background process
        """
        def inner(func:Callable[[], None]):
            self.add_f(process_name, func, auto_start, allow_process_override)            
        return inner
            
    
    def start(self, process_name:str):
        """Start a specific background process.
        
        Args:
            process_name (str): Name of the process to start
        """
        self.threads[process_name].start()
    def destroy(self, process_name:str):
        """Stop a specific background process.
        
        Args:
            process_name (str): Name of the process to stop
        """
        self.threads[process_name].e.set()
    def destroy_all(self):
        """Stop all background processes.
        
        This method is automatically called when the window closes.
        """
        for v in self.threads.values():
            v.e.set()

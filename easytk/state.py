from tkinter import StringVar, IntVar, Tk, Toplevel
from typing import cast, Dict, Callable

class ETKState:
    """A wrapper for tkinter StringVar and IntVar that provides a unified interface.
    
    This class automatically determines whether to use StringVar or IntVar based on
    the type of the initial value provided.
    """
    _v: StringVar | IntVar
    def __init__(self, master:Tk|Toplevel, val:str|int=""):
        """Initialize the state variable.
        
        Args:
            master (Tk | Toplevel): The tkinter window that owns this variable
            val (str | int, optional): Initial value for the variable. Defaults to "".
            
        Raises:
            ValueError: If val is not a string or integer
        """
        if isinstance(val, str):
            self._v = StringVar(master, val)
        elif isinstance(val, int):
            self._v = IntVar(master, val)
        else:
            raise ValueError("ERR @ ETKState.__init__ -> val must be of type str on int")
    
    @property
    def v(self): return self._v.get()
    
    @v.setter
    def v(self, val:int|str) -> None:
        if isinstance(val, int) and isinstance(self._v, IntVar):
            val = cast(int, val)
            var = cast(IntVar, self._v)
            var.set(val)
        elif isinstance(val, str) and isinstance(self._v, StringVar):
            val = cast(int, val)
            var = cast(IntVar, self._v)
            var.set(val)
        else:
            raise ValueError("ERR @ ETKState.v (setter) -> Incompatible types")
        
    def on_change(self):
        """Decorate a function to run every time a state changes
        Args:
            state_name (str): Name of the state variable to bind the function to
        
        """
        def inner(func:Callable[[int|str], None]):
            self._v.trace_add("write", lambda *args: func(self._v.get()))
        return inner
        

class ETKStateManager:
    """Manages multiple ETKState variables for an ETKWindow.
    
    This class provides a centralized way to create and access state variables
    that can be bound to GUI widgets.
    """
    state: Dict[str, ETKState]
    master: Tk | Toplevel
    def __init__(self, master:Tk|Toplevel):
        """Initialize the state manager.
        
        Args:
            master (Tk | Toplevel): The tkinter window that will own the state variables
        """
        self.state = {}
        self.master = master
    def add(self, name:str, val:int|str=""):
        """Add a new state variable.
        
        Args:
            name (str): Unique name to identify the state variable
            val (int | str, optional): Initial value for the variable. Defaults to "".
            
        Raises:
            Exception: If a state variable with the same name already exists
        """
        if name not in self.state:
            self.state[name] = ETKState(self.master, val)
            return
        raise Exception(f"State with name \"{name}\" already exists")
    
    def get(self, name:str): 
        """Get a state variable by name.
        
        Args:
            name (str): Name of the state variable to retrieve
            
        Returns:
            ETKState: The state variable
        """
        return self.__getitem__(name)
    
    def __getitem__(self, key:str) -> (ETKState):
        """Get a state variable using dictionary-style access.
        
        Args:
            key (str): Name of the state variable to retrieve
            
        Returns:
            ETKState: The state variable
            
        Raises:
            KeyError: If no state variable with the given name exists
        """
        if key in self.state: return self.state[key]
        raise KeyError
    
    def on_change(self, state_name:str):
        def inner(func):
            self.state[state_name].on_change()(func)
        return inner

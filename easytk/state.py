from tkinter import StringVar, IntVar, Tk, Toplevel
from typing import cast, Dict

class ETKState:
    _v: StringVar | IntVar
    def __init__(self, master:Tk|Toplevel, val:str|int=""):
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
        

class ETKStateManager:
    state: Dict[str, ETKState]
    master: Tk | Toplevel
    def __init__(self, master:Tk|Toplevel):
        self.state = {}
        self.master = master
    def add(self, name:str, val:int|str=""):
        if name not in self.state:
            self.state[name] = ETKState(self.master, val)
            return
        raise Exception(f"State with name \"{name}\" already exists")
    
    def get(self, name:str): return self.__getitem__(name)
    
    def __getitem__(self, key:str) -> (ETKState):
        if key in self.state: return self.state[key]
        raise KeyError
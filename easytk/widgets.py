from tkinter import Label, Entry, Button, StringVar, IntVar
from typing import TypeVar, Dict, Callable, cast
from easytk.state import ETKState

WT = TypeVar("WT", Label, Entry, Button)
class ETKWidgetManager:
    widgets: Dict[str, (Label | Entry | Button)]
    _last_add:str
    def __init__(self):
        self.widgets = {}
        self._last_add = ""
    
    def add(self, name:str, wid:WT, *after_funcs:Callable[[WT], None]):
        if name not in self.widgets:
            self._last_add = name
            self.widgets[name] = wid
            [f(wid) for f in after_funcs]
    
    def get(self, name:str) -> WT: 
        return self.widgets[name] # type: ignore
    @property
    def last(self) -> WT: 
        if self._last_add != "":
            return self.widgets[self._last_add] # type: ignore
        else:
            raise Exception("ERR - No widgets have been added yet!")
    
    def __getitem__(self, key:str) -> WT:
        if key in self.widgets: return self.widgets[key] # type: ignore
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
    def config(self, wid_name:str): return self.widgets[wid_name].config()
    def in_config(self, wid_name:str, config_name:str) -> bool: return config_name in self.config(wid_name).keys() # type: ignore
    def bind_state(self, wid_name:str, state:ETKState): 
        if self.in_config(wid_name, "textvariable"):
            if isinstance(state._v, StringVar):
                self.widgets[wid_name].config(textvariable=state._v)
                return
            else:
                raise ValueError("ERR @ ETKWidgetManager.bind_state() -> Incompatitble types")
        raise ValueError("ERR @ ETKWidgetManager.bind_state() -> Widget cant have state assigned to it")
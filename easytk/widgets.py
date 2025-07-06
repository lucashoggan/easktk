from tkinter import Label, Entry, Button, StringVar, IntVar, Text, Listbox, Scale, Checkbutton, Radiobutton, Canvas, Frame, Tk, Toplevel, Event
from typing import Union, Dict, Callable, cast, List
from easytk.state import ETKState

# Define all supported widget types in one place
SupportedWidget = Union[
    Label, Entry, Button, Text, Listbox, Scale, 
    Checkbutton, Radiobutton, Canvas, Frame
]


class ETKWidgetManager:
    """Manages GUI widgets for an ETKWindow.
    
    This class provides a centralized way to store, retrieve, and manipulate
    tkinter widgets with additional functionality like placeholders and state binding.
    """
    widgets: Dict[str, SupportedWidget]
    tags: Dict[str, List[str]]
    _last_add:str
    def __init__(self):
        """Initialize the widget manager with an empty widget dictionary."""
        self.widgets = {}
        self.tags = {}
        self._last_add = ""
    
    def add(self, name:str, wid:SupportedWidget, *after_funcs:Callable[[SupportedWidget], None], tags:List[str]=[]):
        """Add a widget to the manager.
        
        Args:
            name (str): Unique name to identify the widget
            wid (SupportedWidget): The tkinter widget to add
            *after_funcs (Callable[[SupportedWidget], None]): Optional functions to call on the widget after adding
        """
        if name not in self.widgets:
            self._last_add = name
            self.widgets[name] = wid
            [f(wid) for f in after_funcs]
            for t in tags:
                if t in self.tags:
                    self.tags[t].append(name)
                else:
                    self.tags[t] = [name]
    
    def get(self, name:str) -> SupportedWidget: 
        """Get a widget by name.
        
        Args:
            name (str): Name of the widget to retrieve
            
        Returns:
            SupportedWidget: The requested widget
        """
        return self.widgets[name]
    
    @property
    def last(self) -> SupportedWidget: 
        """Get the last widget that was added.
        
        Returns:
            SupportedWidget: The most recently added widget
            
        Raises:
            Exception: If no widgets have been added yet
        """
        if self._last_add != "":
            return self.widgets[self._last_add]
        else:
            raise Exception("ERR - No widgets have been added yet!")
    
    def __getitem__(self, key:str) -> SupportedWidget:
        """Get a widget using dictionary-style access.
        
        Args:
            key (str): Name of the widget to retrieve
            
        Returns:
            SupportedWidget: The requested widget
            
        Raises:
            KeyError: If no widget with the given name exists
        """
        if key in self.widgets: return self.widgets[key]
        raise KeyError
    
    def ent_placeholder(self, ent_name:str, placeholder_txt:str, txt_clr:str="black", placeholder_clr:str="grey", show_important:bool=False): # type: ignore
        """Add placeholder text functionality to an Entry widget.
        
        Args:
            ent_name (str): Name of the Entry widget
            placeholder_txt (str): Text to display as placeholder
            txt_clr (str, optional): Color for regular text. Defaults to "black".
            placeholder_clr (str, optional): Color for placeholder text. Defaults to "grey".
            show_important (bool, optional): Whether to reveal password characters when focused. Defaults to False.
            
        Raises:
            Exception: If widget doesn't exist or isn't an Entry widget
        """
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
    def config(self, wid_name:str): 
        """Get the configuration dictionary for a widget.
        
        Args:
            wid_name (str): Name of the widget
            
        Returns:
            dict: Configuration dictionary for the widget
        """
        return self.widgets[wid_name].config()
    def in_config(self, wid_name:str, config_name:str) -> bool: 
        """Check if a configuration option exists for a widget.
        
        Args:
            wid_name (str): Name of the widget
            config_name (str): Name of the configuration option to check
            
        Returns:
            bool: True if the configuration option exists, False otherwise
        """
        return config_name in self.config(wid_name).keys() # type: ignore
    def bind_state(self, wid_name:str, state:ETKState): 
        """Bind an ETKState variable to a widget's textvariable.
        
        Args:
            wid_name (str): Name of the widget to bind to
            state (ETKState): State variable to bind
            
        Raises:
            ValueError: If the widget doesn't support textvariable or types are incompatible
        """
        if self.in_config(wid_name, "textvariable"):
            if isinstance(state._v, StringVar):
                self.widgets[wid_name].config(textvariable=state._v) # type: ignore
                return
            else:
                raise ValueError("ERR @ ETKWidgetManager.bind_state() -> Incompatitble types")
        raise ValueError("ERR @ ETKWidgetManager.bind_state() -> Widget cant have state assigned to it")
    
    def get_widgets_with_tag(self, tag:str) -> List[SupportedWidget]:
        return list(map(lambda x: self.widgets[x], self.tags[tag]))
    
    def add_tag(self, tag:str): 
        if tag in self.tags:
            raise KeyError("ERR @ ETKWidgetManager - Tag with name already exists")
        else:
            self.tags[tag] = []
    def clr_tag(self, tag:str):
        self.tags[tag] = []
    
    def add_widget_to_tag(self, tag:str, wid_name:str):
        if wid_name in self.widgets:
            self.tags[tag].append(wid_name)
            return
        raise KeyError("ERR @ ETKWidgetManager - No widget with such name")
        
    
class ETKFrame:
    widgets: ETKWidgetManager
    master: Tk | Toplevel
    frame: Frame
    def __init__(self, master: Tk | Toplevel):
        self.widgets = ETKWidgetManager()
        self.master = master
        self.frame = Frame(master)
        
    def size(self, x:int, y:int): self.frame.config(width=x, height=y)
    
    @property
    def f(self): return self.frame
        
        
class ETKFrameManager:
    frames: Dict[str, ETKFrame]
    def __init__(self):
        self.frames = {}
    
    def new(self, name:str, frame:ETKFrame, *after_funcs:Callable[[ETKFrame], None], frame_name_overide:bool=False):
        """Bind a new ETKFrame to the ETKFrameManagerClass

        Args:
            name (str): Name of the frame
            frame (ETKFrame): The frame
            frame_name_override (bool): Flag to allow the override of frame names

        Raises:
            KeyError: If frame with that name already exists and frame_name_override flag isn't set to true
        """
        if name in self.frames and not frame_name_overide: raise KeyError("ERR @ ETKFrameManager - Frame already exists with that name, if you want to override this. set the frame_name_override flag to true.")
        self.frames[name] = frame
        for f in after_funcs:
            f(self.frames[name])
            
    def get(self, name:str): return self.frames[name]
    
    def __getitem__(self, key:str): return self.frames[key]
    
        
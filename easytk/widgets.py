from tkinter import Label, Entry, Button, StringVar, IntVar, Text, Listbox, Scale, Checkbutton, Radiobutton, Canvas, Frame, Tk, Toplevel, Event
from typing import Union, Dict, Callable, cast, Optional
from easytk.state import ETKState

# Define all supported widget types in one place
SupportedWidget = Union[
    Label, Entry, Button, Text, Listbox, Scale, 
    Checkbutton, Radiobutton, Canvas, Frame
]

def _bind_event_func(bind_type:str, widget:SupportedWidget, func:Callable[[Event], None]):
    widget.bind(bind_type, func)

def _on_keypress(widget:SupportedWidget, func:Callable[[Event], None],key:Optional[str]=None):
    _bind_event_func(f"<KeyPress-{key}>" if key else "<KeyPress>", widget, func)

def _on_keyrelease(widget:SupportedWidget, func:Callable[[Event], None], key:Optional[str]=None):
    _bind_event_func(f"<KeyRelease-{key}>" if key else "<KeyRelease>", widget, func)

def _on_mousewheel(widget:SupportedWidget, func:Callable[[Event], None]):
    # Handle both Windows and Mac scroll events
    _bind_event_func("<MouseWheel>", widget, func)  # Windows
    _bind_event_func("<Button-4>", widget, func)    # Linux/Mac scroll up
    _bind_event_func("<Button-5>", widget, func)    # Linux/Mac scroll down

def _on_mouse_button(widget:SupportedWidget, func:Callable[[Event], None], button:int, event_type:str="Button"):
    _bind_event_func(f"<{event_type}-{button}>", widget, func)

def _on_focus_event(widget:SupportedWidget, func:Callable[[Event], None], focus_type:str):
    _bind_event_func(f"<{focus_type}>", widget, func)

class ETKWidgetManager:
    """Manages GUI widgets for an ETKWindow.
    
    This class provides a centralized way to store, retrieve, and manipulate
    tkinter widgets with additional functionality like placeholders and state binding.
    """
    widgets: Dict[str, SupportedWidget]
    _last_add:str
    def __init__(self):
        """Initialize the widget manager with an empty widget dictionary."""
        self.widgets = {}
        self._last_add = ""
    
    def add(self, name:str, wid:SupportedWidget, *after_funcs:Callable[[SupportedWidget], None]):
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
    def on_keypress(self, wid_name:str, key:Optional[str]=None):
        """Decorator ind a function to a certian keypress or all keypresses

        Args:
            wid_name (str): Widget name inside manager
            key (Optional[str], optional): Keypress combination, if set to None, all keypresses are registered.     

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_keypress(self.widgets[wid_name], func, key)
        return inner
    def on_mouseover(self, wid_name:str):
        """Decorator to bind onmouseover event on a widget

        Args:
            wid_name (str): Name of widget in manager.

        Raises:
            KeyError: If wid_name not is manager.
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Enter>", self.widgets[wid_name], func)
        return inner
    def on_mouseout(self, wid_name:str):
        """Decorator to bind function to when mouse moves out of widget.

        Args:
            wid_name (str): Name of widget to bind to
        """
        def inner(func: Callable[[Event], None]): _bind_event_func("<Leave>", self.widgets[wid_name], func)
        return inner
    def on_double_left_click(self, wid_name:str):
        """Decorator to bind function to double left click

        Args:
            wid_name (str): _description_
        """
        def inner(func:Callable[[Event], None]): _bind_event_func("<Double-Button-1>", self.widgets[wid_name], func)
        return inner
    def on_double_right_click(self, wid_name:str):
        """Decorator to bind function to double right click

        Args:
            wid_name (str): _description_
        """
        def inner(func:Callable[[Event], None]): _bind_event_func("<Double-Button-2>", self.widgets[wid_name], func)
        return inner
    
    def on_keyrelease(self, wid_name:str, key:Optional[str]=None):
        """Decorator to bind a function to key release events

        Args:
            wid_name (str): Widget name inside manager
            key (Optional[str], optional): Key release combination, if set to None, all key releases are registered.

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_keyrelease(self.widgets[wid_name], func, key)
        return inner
    
    def on_mousewheel(self, wid_name:str):
        """Decorator to bind function to mouse wheel scroll events

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mousewheel(self.widgets[wid_name], func)
        return inner
    
    
    def on_button_press(self, wid_name:str, button:int):
        """Decorator to bind function to specific mouse button press

        Args:
            wid_name (str): Widget name inside manager
            button (int): Mouse button number (1=left, 2=middle, 3=right)

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mouse_button(self.widgets[wid_name], func, button, "Button")
        return inner
    
    def on_button_release(self, wid_name:str, button:int):
        """Decorator to bind function to specific mouse button release

        Args:
            wid_name (str): Widget name inside manager
            button (int): Mouse button number (1=left, 2=middle, 3=right)

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mouse_button(self.widgets[wid_name], func, button, "ButtonRelease")
        return inner
    
    def on_focus_in(self, wid_name:str):
        """Decorator to bind function to widget gaining focus

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_focus_event(self.widgets[wid_name], func, "FocusIn")
        return inner
    
    def on_focus_out(self, wid_name:str):
        """Decorator to bind function to widget losing focus

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _on_focus_event(self.widgets[wid_name], func, "FocusOut")
        return inner
    
    def on_mouse_motion(self, wid_name:str):
        """Decorator to bind function to mouse motion over widget

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Motion>", self.widgets[wid_name], func)
        return inner
    
    def on_configure(self, wid_name:str):
        """Decorator to bind function to widget size/position changes

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Configure>", self.widgets[wid_name], func)
        return inner
    
    def on_destroy(self, wid_name:str):
        """Decorator to bind function to widget destruction

        Args:
            wid_name (str): Widget name inside manager

        Raises:
            KeyError: If widget name not in widget list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Destroy>", self.widgets[wid_name], func)
        return inner
        
    
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
    
    def on_keypress(self, frame_name:str, key:Optional[str]=None):
        """Decorator to bind a function to keypress events on a frame

        Args:
            frame_name (str): Frame name in manager
            key (Optional[str], optional): Keypress combination, if set to None, all keypresses are registered.

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_keypress(self.frames[frame_name].frame, func, key)
        return inner
    
    def on_keyrelease(self, frame_name:str, key:Optional[str]=None):
        """Decorator to bind a function to key release events on a frame

        Args:
            frame_name (str): Frame name in manager
            key (Optional[str], optional): Key release combination, if set to None, all key releases are registered.

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_keyrelease(self.frames[frame_name].frame, func, key)
        return inner
    
    def on_mouseover(self, frame_name:str):
        """Decorator to bind onmouseover event on a frame

        Args:
            frame_name (str): Name of frame in manager.

        Raises:
            KeyError: If frame_name not in manager.
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Enter>", self.frames[frame_name].frame, func)
        return inner
    
    def on_mouseout(self, frame_name:str):
        """Decorator to bind function to when mouse moves out of frame.

        Args:
            frame_name (str): Name of frame to bind to
        """
        def inner(func: Callable[[Event], None]): 
            _bind_event_func("<Leave>", self.frames[frame_name].frame, func)
        return inner
    
    
    
    
    def on_double_left_click(self, frame_name:str):
        """Decorator to bind function to double left click on frame

        Args:
            frame_name (str): Name of frame
        """
        def inner(func:Callable[[Event], None]): 
            _bind_event_func("<Double-Button-1>", self.frames[frame_name].frame, func)
        return inner
    
    def on_double_right_click(self, frame_name:str):
        """Decorator to bind function to double right click on frame

        Args:
            frame_name (str): Name of frame
        """
        def inner(func:Callable[[Event], None]): 
            _bind_event_func("<Double-Button-2>", self.frames[frame_name].frame, func)
        return inner
    
    def on_mousewheel(self, frame_name:str):
        """Decorator to bind function to mouse wheel scroll events on frame

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mousewheel(self.frames[frame_name].frame, func)
        return inner
    
    def on_button_press(self, frame_name:str, button:int):
        """Decorator to bind function to specific mouse button press on frame

        Args:
            frame_name (str): Frame name in manager
            button (int): Mouse button number (1=left, 2=middle, 3=right)

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mouse_button(self.frames[frame_name].frame, func, button, "Button")
        return inner
    
    def on_button_release(self, frame_name:str, button:int):
        """Decorator to bind function to specific mouse button release on frame

        Args:
            frame_name (str): Frame name in manager
            button (int): Mouse button number (1=left, 2=middle, 3=right)

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_mouse_button(self.frames[frame_name].frame, func, button, "ButtonRelease")
        return inner
    
    def on_focus_in(self, frame_name:str):
        """Decorator to bind function to frame gaining focus

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_focus_event(self.frames[frame_name].frame, func, "FocusIn")
        return inner
    
    def on_focus_out(self, frame_name:str):
        """Decorator to bind function to frame losing focus

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _on_focus_event(self.frames[frame_name].frame, func, "FocusOut")
        return inner
    
    def on_mouse_motion(self, frame_name:str):
        """Decorator to bind function to mouse motion over frame

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Motion>", self.frames[frame_name].frame, func)
        return inner
    
    def on_configure(self, frame_name:str):
        """Decorator to bind function to frame size/position changes

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Configure>", self.frames[frame_name].frame, func)
        return inner
    
    def on_destroy(self, frame_name:str):
        """Decorator to bind function to frame destruction

        Args:
            frame_name (str): Frame name in manager

        Raises:
            KeyError: If frame name not in frame list.
        """
        def inner(func:Callable[[Event], None]):
            _bind_event_func("<Destroy>", self.frames[frame_name].frame, func)
        return inner
        
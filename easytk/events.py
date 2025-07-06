from tkinter import Event
from typing import Callable, Optional
from easytk.widgets import SupportedWidget

def _bind_event_func(bind_type: str, widget: SupportedWidget, func: Callable[[Event], None]):
    """Helper function to bind event functions to widgets"""
    widget.bind(bind_type, func)

def _on_keypress(widget: SupportedWidget, func: Callable[[Event], None], key: Optional[str] = None):
    """Helper function for keypress events"""
    _bind_event_func(f"<KeyPress-{key}>" if key else "<KeyPress>", widget, func)

def _on_keyrelease(widget: SupportedWidget, func: Callable[[Event], None], key: Optional[str] = None):
    """Helper function for key release events"""
    _bind_event_func(f"<KeyRelease-{key}>" if key else "<KeyRelease>", widget, func)

def _on_mousewheel(widget: SupportedWidget, func: Callable[[Event], None]):
    """Helper function for mouse wheel events"""
    # Handle both Windows and Mac scroll events
    _bind_event_func("<MouseWheel>", widget, func)  # Windows
    _bind_event_func("<Button-4>", widget, func)    # Linux/Mac scroll up
    _bind_event_func("<Button-5>", widget, func)    # Linux/Mac scroll down

def _on_mouse_button(widget: SupportedWidget, func: Callable[[Event], None], button: int, event_type: str = "Button"):
    """Helper function for mouse button events"""
    _bind_event_func(f"<{event_type}-{button}>", widget, func)

def _on_focus_event(widget: SupportedWidget, func: Callable[[Event], None], focus_type: str):
    """Helper function for focus events"""
    _bind_event_func(f"<{focus_type}>", widget, func)


class ETKEventManager:
    """Centralized event management for EasyTK widgets.
    
    This class provides a unified interface for binding event handlers to widgets
    using decorators. It supports all common tkinter events including mouse,
    keyboard, focus, and lifecycle events.
    """
    
    def __init__(self):
        """Initialize the event manager."""
        pass
    
    def on_keypress(self, widget: SupportedWidget, key: Optional[str] = None):
        """Decorator to bind a function to keypress events on a widget
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
            key (Optional[str], optional): Specific key to bind to. If None, all keypresses are registered.
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_keypress(widget, func, key)
            return func
        return inner
    
    def on_keyrelease(self, widget: SupportedWidget, key: Optional[str] = None):
        """Decorator to bind a function to key release events on a widget
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
            key (Optional[str], optional): Specific key to bind to. If None, all key releases are registered.
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_keyrelease(widget, func, key)
            return func
        return inner
    
    def on_mouseover(self, widget: SupportedWidget):
        """Decorator to bind function to mouse enter events on a widget
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Enter>", widget, func)
            return func
        return inner
    
    def on_mouseout(self, widget: SupportedWidget):
        """Decorator to bind function to mouse leave events on a widget
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Leave>", widget, func)
            return func
        return inner
    
    def on_button_press(self, widget: SupportedWidget, button: int):
        """Decorator to bind function to specific mouse button press events
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
            button (int): Mouse button number (1=left, 2=middle, 3=right)
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_mouse_button(widget, func, button, "Button")
            return func
        return inner
    
    def on_button_release(self, widget: SupportedWidget, button: int):
        """Decorator to bind function to specific mouse button release events
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
            button (int): Mouse button number (1=left, 2=middle, 3=right)
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_mouse_button(widget, func, button, "ButtonRelease")
            return func
        return inner
    
    def on_double_left_click(self, widget: SupportedWidget):
        """Decorator to bind function to double left-click events
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Double-Button-1>", widget, func)
            return func
        return inner
    
    def on_double_right_click(self, widget: SupportedWidget):
        """Decorator to bind function to double right-click events
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Double-Button-2>", widget, func)
            return func
        return inner
    
    def on_mousewheel(self, widget: SupportedWidget):
        """Decorator to bind function to mouse wheel scroll events
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_mousewheel(widget, func)
            return func
        return inner
    
    def on_focus_in(self, widget: SupportedWidget):
        """Decorator to bind function to widget gaining focus
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_focus_event(widget, func, "FocusIn")
            return func
        return inner
    
    def on_focus_out(self, widget: SupportedWidget):
        """Decorator to bind function to widget losing focus
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _on_focus_event(widget, func, "FocusOut")
            return func
        return inner
    
    def on_mouse_motion(self, widget: SupportedWidget):
        """Decorator to bind function to mouse motion over widget
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Motion>", widget, func)
            return func
        return inner
    
    def on_configure(self, widget: SupportedWidget):
        """Decorator to bind function to widget size/position changes
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Configure>", widget, func)
            return func
        return inner
    
    def on_destroy(self, widget: SupportedWidget):
        """Decorator to bind function to widget destruction
        
        Args:
            widget (SupportedWidget): The widget to bind the event to
        
        Returns:
            Callable: Decorator function
        """
        def inner(func: Callable[[Event], None]):
            _bind_event_func("<Destroy>", widget, func)
            return func
        return inner

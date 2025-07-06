#!/usr/bin/env python3
"""
Test file for the new ETKEventManager.
This demonstrates how to use the centralized event manager with widget instances.
"""

from tkinter import Tk, Label, Button, Entry, Text, Canvas
from easytk.window import ETKWindow
import time

def main():
    window = ETKWindow(Tk())
    window.title("ETKEventManager Test").geometry("800x600")
    
    # Create a text widget to show event messages
    window.widgets.add(
        "event_log",
        Text(window.m, height=15, width=50, wrap="word"),
        lambda w: w.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    )
    
    def log_event(message):
        """Helper function to log events"""
        timestamp = time.strftime("%H:%M:%S")
        window.widgets["event_log"].insert("end", f"[{timestamp}] {message}\n")
        window.widgets["event_log"].see("end")
    
    # Create test widgets
    window.widgets.add(
        "test_label",
        Label(window.m, text="Hover over me!", bg="lightblue", pady=10),
        lambda w: w.pack(pady=5, fill="x", padx=10)
    )
    
    window.widgets.add(
        "test_button",
        Button(window.m, text="Click me with different mouse buttons!", bg="lightgreen"),
        lambda w: w.pack(pady=5, fill="x", padx=10)
    )
    
    window.widgets.add(
        "test_entry",
        Entry(window.m, width=40),
        lambda w: w.pack(pady=5, padx=10),
        lambda w: w.insert(0, "Type here and press keys...")
    )
    
    window.widgets.add(
        "test_canvas",
        Canvas(window.m, height=100, bg="white", relief="sunken", bd=2),
        lambda w: w.pack(pady=5, fill="x", padx=10)
    )
    
    # === NEW EVENT MANAGER USAGE ===
    
    # Mouse events using the new event manager with widget instances
    @window.events.on_mouseover(window.widgets["test_label"])
    def on_label_hover(event):
        log_event("🖱️ Mouse entered label (via ETKEventManager)")
        window.widgets["test_label"].config(bg="yellow")
    
    @window.events.on_mouseout(window.widgets["test_label"])
    def on_label_leave(event):
        log_event("🖱️ Mouse left label (via ETKEventManager)")
        window.widgets["test_label"].config(bg="lightblue")
    
    @window.events.on_button_press(window.widgets["test_button"], 1)
    def on_left_click(event):
        log_event("👆 Left click on button (via ETKEventManager)")

    @window.events.on_button_press(window.widgets["test_button"], 3)
    def on_right_click(event):
        log_event("👆 Right click on button (via ETKEventManager)")

    @window.events.on_button_press(window.widgets["test_button"], 2)
    def on_middle_click(event):
        log_event("🖱️ Middle mouse button clicked! (via ETKEventManager)")
    
    @window.events.on_double_left_click(window.widgets["test_button"])
    def on_double_left_click(event):
        log_event("👆👆 Double left click on button (via ETKEventManager)")
    
    @window.events.on_double_right_click(window.widgets["test_button"])
    def on_double_right_click(event):
        log_event("👆👆 Double right click on button (via ETKEventManager)")
    
    # Keyboard events
    @window.events.on_keypress(window.widgets["test_entry"])
    def on_any_keypress(event):
        log_event(f"⌨️ Key pressed: {event.keysym} (via ETKEventManager)")
    
    @window.events.on_keypress(window.widgets["test_entry"], "Return")
    def on_enter_press(event):
        log_event("⌨️ Enter key pressed! (via ETKEventManager)")
    
    @window.events.on_keypress(window.widgets["test_entry"], "Escape")
    def on_escape_press(event):
        log_event("⌨️ Escape key pressed! (via ETKEventManager)")
        window.widgets["test_entry"].delete(0, "end")
    
    @window.events.on_keyrelease(window.widgets["test_entry"])
    def on_key_release(event):
        log_event(f"⌨️⬆️ Key released: {event.keysym} (via ETKEventManager)")
    
    @window.events.on_keyrelease(window.widgets["test_entry"], "space")
    def on_space_release(event):
        log_event("⌨️⬆️ Space key released! (via ETKEventManager)")
    
    # Mouse wheel and advanced events
    @window.events.on_mousewheel(window.widgets["test_canvas"])
    def on_mouse_wheel(event):
        direction = "up" if event.delta > 0 else "down"
        log_event(f"🎡 Mouse wheel scrolled {direction} on canvas (via ETKEventManager)")
    
    @window.events.on_button_press(window.widgets["test_canvas"], 1)
    def on_canvas_left_press(event):
        log_event(f"🎨 Left button pressed on canvas at ({event.x}, {event.y}) (via ETKEventManager)")
    
    @window.events.on_button_release(window.widgets["test_canvas"], 1)
    def on_canvas_left_release(event):
        log_event(f"🎨 Left button released on canvas at ({event.x}, {event.y}) (via ETKEventManager)")
    
    # Focus events
    @window.events.on_focus_in(window.widgets["test_entry"])
    def on_entry_focus_in(event):
        log_event("🎯 Entry widget gained focus (via ETKEventManager)")
        window.widgets["test_entry"].config(bg="lightyellow")
    
    @window.events.on_focus_out(window.widgets["test_entry"])
    def on_entry_focus_out(event):
        log_event("🎯 Entry widget lost focus (via ETKEventManager)")
        window.widgets["test_entry"].config(bg="white")
    
    # Motion and configure events
    @window.events.on_mouse_motion(window.widgets["test_canvas"])
    def on_canvas_mouse_motion(event):
        # Only log every 20th motion event to avoid spam
        if hasattr(on_canvas_mouse_motion, 'counter'):
            on_canvas_mouse_motion.counter += 1
        else:
            on_canvas_mouse_motion.counter = 1
        
        if on_canvas_mouse_motion.counter % 20 == 0:
            log_event(f"🖱️ Mouse moving on canvas: ({event.x}, {event.y}) (via ETKEventManager)")
    
    @window.events.on_configure(window.widgets["test_canvas"])
    def on_canvas_configure(event):
        log_event(f"📐 Canvas resized to {event.width}x{event.height} (via ETKEventManager)")
    
    # Add instructions
    window.widgets.add(
        "instructions",
        Label(
            window.m, 
            text="NEW ETKEventManager Demo:\\n" +
                 "• All events now use window.events.on_*() with widget instances\\n" +
                 "• More direct and flexible than widget name strings\\n" +
                 "• Centralized event management\\n" +
                 "• Same functionality as before but cleaner API\\n\\n" +
                 "Try interacting with the widgets above!",
            justify="left",
            bg="lightgreen",
            pady=10
        ),
        lambda w: w.pack(side="bottom", fill="x", padx=10, pady=10)
    )
    
    # Add initial log message
    log_event("🚀 ETKEventManager testing started! All events use the new centralized manager.")
    
    window.run()

if __name__ == "__main__":
    main()

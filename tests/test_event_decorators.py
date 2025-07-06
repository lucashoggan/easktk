#!/usr/bin/env python3
"""
Test file for all ETKWidgetManager event decorators.
This demonstrates all the available event binding decorators.
"""

from tkinter import Tk, Label, Button, Entry, Text, Canvas, Listbox
from easytk.window import ETKWindow
import time

def main():
    window = ETKWindow(Tk())
    window.title("Event Decorators Test").geometry("800x600")
    
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
    
    window.widgets.add(
        "test_listbox",
        Listbox(window.m, height=4),
        lambda w: w.pack(pady=5, fill="x", padx=10),
        lambda w: [w.insert("end", f"Item {i}") for i in range(1, 6)]
    )
    
    # === EXISTING EVENT DECORATORS ===
    
    @window.widgets.on_mouseover("test_label")
    def on_label_hover(event):
        log_event("🖱️ Mouse entered label")
        window.widgets["test_label"].config(bg="yellow")
    
    @window.widgets.on_mouseout("test_label")
    def on_label_leave(event):
        log_event("🖱️ Mouse left label")
        window.widgets["test_label"].config(bg="lightblue")
    
    @window.widgets.on_button_press("test_button", 1)
    def on_left_click(event):
        log_event("👆 Left click on button")

    @window.widgets.on_button_press("test_button", 2)
    def on_right_click(event):
        log_event("👆 Right click on button")
    @window.widgets.on_double_left_click("test_button")
    def on_double_left_click(event):
        log_event("👆👆 Double left click on button")
    
    @window.widgets.on_double_right_click("test_button")
    def on_double_right_click(event):
        log_event("👆👆 Double right click on button")
    
    @window.widgets.on_keypress("test_entry")
    def on_any_keypress(event):
        log_event(f"⌨️ Key pressed: {event.keysym}")
    
    @window.widgets.on_keypress("test_entry", "Return")
    def on_enter_press(event):
        log_event("⌨️ Enter key pressed!")
    
    @window.widgets.on_keypress("test_entry", "Escape")
    def on_escape_press(event):
        log_event("⌨️ Escape key pressed!")
        window.widgets["test_entry"].delete(0, "end")
    
    # === NEW EVENT DECORATORS ===
    
    @window.widgets.on_keyrelease("test_entry")
    def on_key_release(event):
        log_event(f"⌨️⬆️ Key released: {event.keysym}")
    
    @window.widgets.on_keyrelease("test_entry", "space")
    def on_space_release(event):
        log_event("⌨️⬆️ Space key released!")
    
    @window.widgets.on_mousewheel("test_canvas")
    def on_mouse_wheel(event):
        # event.delta gives scroll direction (positive = up, negative = down)
        direction = "up" if event.delta > 0 else "down"
        log_event(f"🎡 Mouse wheel scrolled {direction} on canvas")
    
    @window.widgets.on_button_press("test_button", 3)
    def on_middle_click(event):
        log_event("🖱️ Middle mouse button clicked!")
    
    @window.widgets.on_button_press("test_canvas", 1)
    def on_canvas_left_press(event):
        log_event(f"🎨 Left button pressed on canvas at ({event.x}, {event.y})")
    
    @window.widgets.on_button_press("test_canvas", 3)
    def on_canvas_right_press(event):
        log_event(f"🎨 Right button pressed on canvas at ({event.x}, {event.y})")
    
    @window.widgets.on_button_release("test_canvas", 1)
    def on_canvas_left_release(event):
        log_event(f"🎨 Left button released on canvas at ({event.x}, {event.y})")
    
    @window.widgets.on_focus_in("test_entry")
    def on_entry_focus_in(event):
        log_event("🎯 Entry widget gained focus")
        window.widgets["test_entry"].config(bg="lightyellow")
    
    @window.widgets.on_focus_out("test_entry")
    def on_entry_focus_out(event):
        log_event("🎯 Entry widget lost focus")
        window.widgets["test_entry"].config(bg="white")
    
    @window.widgets.on_mouse_motion("test_canvas")
    def on_canvas_mouse_motion(event):
        # Only log every 10th motion event to avoid spam
        if hasattr(on_canvas_mouse_motion, 'counter'):
            on_canvas_mouse_motion.counter += 1
        else:
            on_canvas_mouse_motion.counter = 1
        
        if on_canvas_mouse_motion.counter % 20 == 0:
            log_event(f"🖱️ Mouse moving on canvas: ({event.x}, {event.y})")
    
    @window.widgets.on_configure("test_canvas")
    def on_canvas_configure(event):
        log_event(f"📐 Canvas resized to {event.width}x{event.height}")
    
    @window.widgets.on_destroy("test_button")
    def on_button_destroy(event):
        log_event("💥 Button widget was destroyed!")
    
    # Add some instructions
    window.widgets.add(
        "instructions",
        Label(
            window.m, 
            text="Try different interactions with the widgets above:\n" +
                 "• Hover over the blue label\n" +
                 "• Click the button with left, right, middle mouse buttons\n" +
                 "• Double-click the button\n" +
                 "• Type in the entry field\n" +
                 "• Press Enter or Escape in the entry\n" +
                 "• Scroll mouse wheel over the canvas\n" +
                 "• Click and drag on the canvas\n" +
                 "• Click on different widgets to change focus",
            justify="left",
            bg="lightgray",
            pady=10
        ),
        lambda w: w.pack(side="bottom", fill="x", padx=10, pady=10)
    )
    
    # Add initial log message
    log_event("🚀 Event testing started! Try interacting with the widgets.")
    
    window.run()

if __name__ == "__main__":
    main()

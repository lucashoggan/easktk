# ETKWindow Class Documentation

The `ETKWindow` class is the main window container in the EasyTK library, providing a unified interface for managing GUI components, state, and background processes.

## Overview

`ETKWindow` wraps a tkinter `Tk` or `Toplevel` widget and provides five main managers:
- **Widget Manager**: For managing GUI widgets
- **State Manager**: For managing application state
- **Background Process Manager**: For managing background threads
- **Queue Manager**: For thread-safe communication
- **Event Manager**: For centralized event handling

## Constructor

```python
from tkinter import Tk
from easytk.window import ETKWindow

# Create a main window
window = ETKWindow(Tk())
```

### Parameters
- `master` (Tk | Toplevel): The tkinter window to wrap

## Properties

### Core Managers
- `widgets`: ETKWidgetManager - Manages GUI widgets
- `state`: ETKStateManager - Manages application state variables
- `processes`: ETKBackgroundProcessManager - Manages background threads
- `queue`: ETKQueueManager - Manages thread-safe task queue
- `events`: ETKEventManager - Manages centralized event handling

### Master Access
- `master`: Direct access to the underlying tkinter window
- `m`: Shorthand property for `master`

## Methods

### `sub()`
Creates a child window (Toplevel) of the current window.

```python
# Create a child window
child_window = window.sub()
child_window.run()  # Run the child window
```

**Returns**: `ETKWindow` - A new ETKWindow instance with a Toplevel master

### `run()`
Starts the main event loop and handles cleanup when the window is closed.

```python
# Start the application
window.run()
```

This method:
1. Calls `master.mainloop()` to start the GUI event loop
2. Automatically destroys all background processes when the window closes

### `geometry(geometry_string)`
Sets the window geometry (size and position).

```python
# Set window size
window.geometry("400x300")

# Set window size and position
window.geometry("400x300+100+50")
```

**Parameters:**
- `geometry_string` (str): Geometry in format 'widthxheight+x+y' or 'widthxheight'

**Returns:** `ETKWindow` - Returns self for method chaining

### `title(title)`
Sets the window title.

```python
# Set window title
window.title("My Application")
```

**Parameters:**
- `title` (str): The title to set for the window

**Returns:** `ETKWindow` - Returns self for method chaining

## Usage Examples

### Basic Window Setup

```python
from tkinter import Tk, Label, Button
from easytk.window import ETKWindow

# Create main window
window = ETKWindow(Tk())
window.title("My Application").geometry("400x300")

# Add a label widget and add to manager
window.widgets.add("greeting", Label(window.m, text="Hello World!"))
window.widgets["greeting"].pack(pady=20)

# Run the application
window.run()
```

### Using After-Funcs for Widget Configuration

The `widgets.add()` method accepts optional after-functions that are automatically called on the widget after it's added to the manager. This is useful for packing, configuring, or styling widgets in one line.

```python
from tkinter import Tk, Label, Button, Entry
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("After-Funcs Demo").geometry("400x300")

# Add widgets with after-funcs to pack them automatically
window.widgets.add(
    "title_label", 
    Label(window.m, text="Welcome to EasyTK!", font=("Arial", 16)),
    lambda w: w.pack(pady=20),
    lambda w: w.config(fg="blue")
)

window.widgets.add(
    "username_entry", 
    Entry(window.m, width=30),
    lambda w: w.pack(pady=10),
    lambda w: w.insert(0, "Enter username...")
)

window.widgets.add(
    "submit_btn", 
    Button(window.m, text="Submit", bg="green", fg="white"),
    lambda w: w.pack(pady=10),
    lambda w: w.config(width=20)
)

# Add a label with multiple styling after-funcs
window.widgets.add(
    "status_label", 
    Label(window.m, text="Ready"),
    lambda w: w.pack(side="bottom", pady=10),
    lambda w: w.config(bg="lightgray", relief="sunken", bd=2),
    lambda w: w.config(width=40)
)

window.run()
```
### Tagging widgets
```python
# Adding/Creating tag at widget addition
win.widgets.add("h1", 
    Label(win.m, text="Hello World!"), 
    lambda w: w.pack(),
    tags=["heading"]
)
# Creating tag later
win.widgets.add_tag("text")
# Adding tag to widget later
win.widgets.add_widget_to_tag("text", "h1")

# Select all widgets with tag
for widget in win.widgets.get_widgets_with_tag("text"):
    ...

```

### Using State Management

```python
from tkinter import Tk, Entry, Button
from easytk.window import ETKWindow

window = ETKWindow(Tk())

# Create state variable
window.state.add("username", "")

# Create entry widget with after-func to pack it
window.widgets.add(
    "username_entry", 
    Entry(window.m),
    lambda w: w.pack(pady=10)
)
window.widgets.bind_state("username_entry", window.state["username"])

# Create button to display state with after-func
def show_username():
    print(f"Username: {window.state['username'].v}")

window.widgets.add(
    "show_btn", 
    Button(window.m, text="Show Username", command=show_username),
    lambda w: w.pack(pady=5)
)

window.run()
```

### State Change Listeners

You can use the `on_change` decorators to automatically run functions when state variables change. This is useful for reactive programming patterns.

#### Using ETKState.on_change (Direct State Variable)

```python
from tkinter import Tk, Entry, Label
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("State Change Demo").geometry("400x300")

# Create state variables
window.state.add("username", "")
window.state.add("counter", 0)

# Create widgets
window.widgets.add(
    "username_entry", 
    Entry(window.m, width=30),
    lambda w: w.pack(pady=10)
)
window.widgets.bind_state("username_entry", window.state["username"])

window.widgets.add(
    "display_label", 
    Label(window.m, text="Username: "),
    lambda w: w.pack(pady=10)
)

window.widgets.add(
    "counter_label", 
    Label(window.m, text="Counter: 0"),
    lambda w: w.pack(pady=10)
)

# Use on_change decorator on individual state variables
@window.state["username"].on_change()
def on_username_change(new_value):
    # Update the display label whenever username changes
    window.widgets["display_label"].config(text=f"Username: {new_value}")
    print(f"Username changed to: {new_value}")

@window.state["counter"].on_change()
def on_counter_change(new_value):
    # Update the counter label whenever counter changes
    window.widgets["counter_label"].config(text=f"Counter: {new_value}")
    print(f"Counter changed to: {new_value}")

# Function to increment counter (for demonstration)
def increment_counter():
    window.state["counter"].v += 1

window.widgets.add(
    "increment_btn", 
    Button(window.m, text="Increment Counter", command=increment_counter),
    lambda w: w.pack(pady=10)
)

window.run()
```

#### Using ETKStateManager.on_change (State Manager)

```python
from tkinter import Tk, Entry, Label, Button, Scale
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("State Manager Change Demo").geometry("400x350")

# Create state variables
window.state.add("temperature", 20)
window.state.add("status", "Normal")
window.state.add("name", "")

# Create widgets
window.widgets.add(
    "name_entry", 
    Entry(window.m, width=30),
    lambda w: w.pack(pady=5)
)
window.widgets.bind_state("name_entry", window.state["name"])

window.widgets.add(
    "temp_scale", 
    Scale(window.m, from_=0, to=100, orient="horizontal", length=300),
    lambda w: w.pack(pady=10)
)
window.widgets.bind_state("temp_scale", window.state["temperature"])

window.widgets.add(
    "status_label", 
    Label(window.m, text="Status: Normal", font=("Arial", 12)),
    lambda w: w.pack(pady=10)
)

window.widgets.add(
    "info_label", 
    Label(window.m, text="Enter name and adjust temperature", fg="blue"),
    lambda w: w.pack(pady=10)
)

# Use state manager on_change decorator
@window.state.on_change("temperature")
def on_temperature_change(new_temp):
    # Update status based on temperature
    if new_temp < 10:
        window.state["status"].v = "Cold"
    elif new_temp > 30:
        window.state["status"].v = "Hot"
    else:
        window.state["status"].v = "Normal"
    
    print(f"Temperature changed to: {new_temp}°C")

@window.state.on_change("status")
def on_status_change(new_status):
    # Update label color based on status
    colors = {"Cold": "blue", "Hot": "red", "Normal": "green"}
    color = colors.get(new_status, "black")
    
    window.widgets["status_label"].config(
        text=f"Status: {new_status}",
        fg=color
    )
    print(f"Status changed to: {new_status}")

@window.state.on_change("name")
def on_name_change(new_name):
    # Update info label with personalized message
    if new_name.strip():
        window.widgets["info_label"].config(
            text=f"Hello {new_name}! Adjust the temperature."
        )
    else:
        window.widgets["info_label"].config(
            text="Enter name and adjust temperature"
        )
    print(f"Name changed to: {new_name}")

window.run()
```

#### Complex State Change Example with Multiple Listeners

```python
from tkinter import Tk, Entry, Label, Button, Checkbutton
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("Complex State Changes").geometry("450x400")

# Create state variables
window.state.add("user_input", "")
window.state.add("word_count", 0)
window.state.add("is_valid", 0)  # Using int for boolean (0/1)
window.state.add("validation_message", "")

# Create widgets
window.widgets.add(
    "input_entry", 
    Entry(window.m, width=40),
    lambda w: w.pack(pady=10)
)
window.widgets.bind_state("input_entry", window.state["user_input"])

window.widgets.add(
    "word_count_label", 
    Label(window.m, text="Word count: 0"),
    lambda w: w.pack(pady=5)
)

window.widgets.add(
    "validation_label", 
    Label(window.m, text="Enter some text...", fg="gray"),
    lambda w: w.pack(pady=5)
)

window.widgets.add(
    "valid_checkbox", 
    Checkbutton(window.m, text="Input is valid", state="disabled"),
    lambda w: w.pack(pady=5)
)
window.widgets.bind_state("valid_checkbox", window.state["is_valid"])

# Multiple state change listeners
@window.state.on_change("user_input")
def on_input_change(new_input):
    # Update word count
    words = len(new_input.split()) if new_input.strip() else 0
    window.state["word_count"].v = words
    
    # Update validation
    is_valid = len(new_input.strip()) >= 3 and words >= 2
    window.state["is_valid"].v = 1 if is_valid else 0
    
    # Update validation message
    if not new_input.strip():
        window.state["validation_message"].v = "Enter some text..."
    elif len(new_input.strip()) < 3:
        window.state["validation_message"].v = "Text too short (min 3 chars)"
    elif words < 2:
        window.state["validation_message"].v = "Need at least 2 words"
    else:
        window.state["validation_message"].v = "Valid input!"

@window.state.on_change("word_count")
def on_word_count_change(new_count):
    window.widgets["word_count_label"].config(
        text=f"Word count: {new_count}"
    )

@window.state.on_change("validation_message")
def on_validation_message_change(new_message):
    # Color coding for validation messages
    if "Valid" in new_message:
        color = "green"
    elif "too short" in new_message or "Need at least" in new_message:
        color = "red"
    else:
        color = "gray"
    
    window.widgets["validation_label"].config(
        text=new_message,
        fg=color
    )

@window.state.on_change("is_valid")
def on_validity_change(is_valid):
    print(f"Input validity changed: {bool(is_valid)}")

window.run()
```

### Background Processes (Using add_f method)

```python
from tkinter import Tk, Label
from easytk.window import ETKWindow
import time

window = ETKWindow(Tk())

# Add a label to show updates
window.widgets.add("counter_label", Label(window.m, text="Counter: 0"))
window.widgets["counter_label"].pack(pady=20)

# Create state for counter
window.state.add("counter", 0)

# Background process function
def update_counter():
    current = window.state["counter"].v
    window.state["counter"].v = current + 1
    
    # Use queue to safely update GUI from background thread
    window.queue.add(lambda: window.widgets["counter_label"].config(
        text=f"Counter: {window.state['counter'].v}"
    ))
    
    time.sleep(1)  # Wait 1 second

# Add and start background process
window.processes.add_f("counter_updater", update_counter, auto_start_process=True)

window.run()
```

### Background Processes (Using add decorator)

```python
from tkinter import Tk, Label
from easytk.window import ETKWindow
import time

window = ETKWindow(Tk())

# Add a label to show updates
window.widgets.add("status_label", Label(window.m, text="Status: Ready"))
window.widgets["status_label"].pack(pady=20)

# Create state for status
window.state.add("status", "Ready")

# Use decorator to define background process
@window.processes.add("status_monitor", auto_start=True)
def monitor_status():
    # Simulate some background work
    statuses = ["Working...", "Processing...", "Analyzing...", "Complete"]
    
    for status in statuses:
        window.state["status"].v = status
        
        # Use queue to safely update GUI from background thread
        window.queue.add(lambda s=status: window.widgets["status_label"].config(
            text=f"Status: {s}"
        ))
        
        time.sleep(2)  # Wait 2 seconds between status updates
    
    # Reset to ready after cycle
    window.state["status"].v = "Ready"
    window.queue.add(lambda: window.widgets["status_label"].config(
        text="Status: Ready"
    ))

window.run()
```

### Multiple Background Processes with Decorator

```python
from tkinter import Tk, Label, Frame
from easytk.window import ETKWindow
import time
import random

window = ETKWindow(Tk())
window.title("Multiple Background Processes").geometry("400x200")

# Create UI elements
window.widgets.add("frame", Frame(window.m))
window.widgets["frame"].pack(pady=20)

window.widgets.add("counter_label", Label(window.widgets["frame"], text="Counter: 0"))
window.widgets["counter_label"].pack(pady=5)

window.widgets.add("temp_label", Label(window.widgets["frame"], text="Temperature: 20°C"))
window.widgets["temp_label"].pack(pady=5)

# Create state variables
window.state.add("counter", 0)
window.state.add("temperature", 20)

# Counter process using decorator
@window.processes.add("counter_process", auto_start=True)
def count_up():
    current = window.state["counter"].v
    window.state["counter"].v = current + 1
    
    window.queue.add(lambda: window.widgets["counter_label"].config(
        text=f"Counter: {window.state['counter'].v}"
    ))
    
    time.sleep(1)

# Temperature simulation process using decorator
@window.processes.add("temperature_process", auto_start=True)
def simulate_temperature():
    # Simulate temperature fluctuation
    change = random.uniform(-0.5, 0.5)
    current = window.state["temperature"].v
    new_temp = max(15, min(35, current + change))  # Keep between 15-35°C
    window.state["temperature"].v = int(new_temp)
    
    window.queue.add(lambda: window.widgets["temp_label"].config(
        text=f"Temperature: {window.state['temperature'].v}°C"
    ))
    
    time.sleep(3)  # Update every 3 seconds

window.run()
```

### Frame Management with ETKFrameManager

The ETKFrameManager allows you to organize your GUI into multiple frames, making it easy to create complex layouts, multi-page applications, or modular interfaces. Each ETKFrame has its own widget manager, allowing for clean separation of components.

#### Basic Frame Usage

```python
from tkinter import Tk, Label, Button, Entry
from easytk.window import ETKWindow
from easytk.widgets import ETKFrame

window = ETKWindow(Tk())
window.title("Frame Manager Demo").geometry("500x400")

# Create frames
header_frame = ETKFrame(window.m)
content_frame = ETKFrame(window.m)
footer_frame = ETKFrame(window.m)

# Add frames to the manager with layout configuration
window.frames.new(
    "header", 
    header_frame,
    lambda f: f.f.pack(side="top", fill="x", padx=10, pady=5),
    lambda f: f.f.config(bg="lightblue")
)

window.frames.new(
    "content", 
    content_frame,
    lambda f: f.f.pack(side="top", fill="both", expand=True, padx=10, pady=5),
    lambda f: f.f.config(bg="white")
)

window.frames.new(
    "footer", 
    footer_frame,
    lambda f: f.f.pack(side="bottom", fill="x", padx=10, pady=5),
    lambda f: f.f.config(bg="lightgray")
)

# Add widgets to header frame
window.frames["header"].widgets.add(
    "title",
    Label(window.frames["header"].f, text="My Application", font=("Arial", 16, "bold")),
    lambda w: w.pack(pady=10)
)

# Add widgets to content frame
window.frames["content"].widgets.add(
    "username_label",
    Label(window.frames["content"].f, text="Username:"),
    lambda w: w.pack(pady=5)
)

window.frames["content"].widgets.add(
    "username_entry",
    Entry(window.frames["content"].f, width=30),
    lambda w: w.pack(pady=5)
)

window.frames["content"].widgets.add(
    "submit_btn",
    Button(window.frames["content"].f, text="Submit", bg="green", fg="white"),
    lambda w: w.pack(pady=10)
)

# Add widgets to footer frame
window.frames["footer"].widgets.add(
    "status",
    Label(window.frames["footer"].f, text="Ready", font=("Arial", 10)),
    lambda w: w.pack(pady=5)
)

window.run()
```

#### Multi-Page Application with Frame Switching

```python
from tkinter import Tk, Label, Button, Entry, Text
from easytk.window import ETKWindow
from easytk.widgets import ETKFrame

window = ETKWindow(Tk())
window.title("Multi-Page App").geometry("600x400")

# Create navigation frame
nav_frame = ETKFrame(window.m)
window.frames.new(
    "navigation",
    nav_frame,
    lambda f: f.f.pack(side="top", fill="x", padx=10, pady=5),
    lambda f: f.f.config(bg="navy", height=60)
)

# Create page frames
home_frame = ETKFrame(window.m)
about_frame = ETKFrame(window.m)
contact_frame = ETKFrame(window.m)

# Add page frames (initially hidden)
window.frames.new("home", home_frame)
window.frames.new("about", about_frame)
window.frames.new("contact", contact_frame)

# Track current page
window.state.add("current_page", "home")

# Function to switch pages
def show_page(page_name):
    # Hide all pages
    for page in ["home", "about", "contact"]:
        window.frames[page].f.pack_forget()
    
    # Show selected page
    window.frames[page_name].f.pack(side="top", fill="both", expand=True, padx=10, pady=5)
    window.state["current_page"].v = page_name
    
    # Update navigation button colors
    for btn_name in ["home_btn", "about_btn", "contact_btn"]:
        color = "lightblue" if btn_name.replace("_btn", "") == page_name else "white"
        window.frames["navigation"].widgets[btn_name].config(bg=color)

# Add navigation buttons
window.frames["navigation"].widgets.add(
    "home_btn",
    Button(
        window.frames["navigation"].f, 
        text="Home", 
        command=lambda: show_page("home"),
        bg="lightblue",
        fg="black",
        width=10
    ),
    lambda w: w.pack(side="left", padx=5, pady=10)
)

window.frames["navigation"].widgets.add(
    "about_btn",
    Button(
        window.frames["navigation"].f, 
        text="About", 
        command=lambda: show_page("about"),
        bg="white",
        fg="black",
        width=10
    ),
    lambda w: w.pack(side="left", padx=5, pady=10)
)

window.frames["navigation"].widgets.add(
    "contact_btn",
    Button(
        window.frames["navigation"].f, 
        text="Contact", 
        command=lambda: show_page("contact"),
        bg="white",
        fg="black",
        width=10
    ),
    lambda w: w.pack(side="left", padx=5, pady=10)
)

# Setup Home Page
window.frames["home"].widgets.add(
    "home_title",
    Label(window.frames["home"].f, text="Welcome Home!", font=("Arial", 20, "bold")),
    lambda w: w.pack(pady=20)
)

window.frames["home"].widgets.add(
    "home_content",
    Label(
        window.frames["home"].f, 
        text="This is the home page.\nYou can navigate using the buttons above.",
        font=("Arial", 12),
        justify="center"
    ),
    lambda w: w.pack(pady=10)
)

# Setup About Page
window.frames["about"].widgets.add(
    "about_title",
    Label(window.frames["about"].f, text="About Us", font=("Arial", 20, "bold")),
    lambda w: w.pack(pady=20)
)

window.frames["about"].widgets.add(
    "about_content",
    Text(
        window.frames["about"].f, 
        height=10, 
        width=50,
        wrap="word"
    ),
    lambda w: w.pack(pady=10, padx=20, fill="both", expand=True),
    lambda w: w.insert("1.0", "This is a multi-page application built with EasyTK.\n\n" +
                              "The frame manager allows for easy organization of different " +
                              "sections of your application into separate, manageable frames.\n\n" +
                              "Each frame has its own widget manager, making it easy to " +
                              "organize and manage widgets within specific sections.")
)

# Setup Contact Page
window.frames["contact"].widgets.add(
    "contact_title",
    Label(window.frames["contact"].f, text="Contact Us", font=("Arial", 20, "bold")),
    lambda w: w.pack(pady=20)
)

window.frames["contact"].widgets.add(
    "name_label",
    Label(window.frames["contact"].f, text="Name:"),
    lambda w: w.pack(pady=5)
)

window.frames["contact"].widgets.add(
    "name_entry",
    Entry(window.frames["contact"].f, width=40),
    lambda w: w.pack(pady=5)
)

window.frames["contact"].widgets.add(
    "email_label",
    Label(window.frames["contact"].f, text="Email:"),
    lambda w: w.pack(pady=5)
)

window.frames["contact"].widgets.add(
    "email_entry",
    Entry(window.frames["contact"].f, width=40),
    lambda w: w.pack(pady=5)
)

window.frames["contact"].widgets.add(
    "submit_contact",
    Button(
        window.frames["contact"].f, 
        text="Submit", 
        bg="green", 
        fg="white",
        command=lambda: print("Contact form submitted!")
    ),
    lambda w: w.pack(pady=15)
)

# Show initial page
show_page("home")

window.run()
```

#### Dashboard Layout with Multiple Frames

```python
from tkinter import Tk, Label, Button, Listbox, Text
from easytk.window import ETKWindow
from easytk.widgets import ETKFrame

window = ETKWindow(Tk())
window.title("Dashboard Layout").geometry("800x600")

# Create layout frames
top_frame = ETKFrame(window.m)
left_frame = ETKFrame(window.m)
right_frame = ETKFrame(window.m)
bottom_frame = ETKFrame(window.m)

# Add frames with specific layouts
window.frames.new(
    "top",
    top_frame,
    lambda f: f.f.pack(side="top", fill="x", padx=5, pady=5),
    lambda f: f.f.config(bg="darkblue", height=80)
)

window.frames.new(
    "left",
    left_frame,
    lambda f: f.f.pack(side="left", fill="y", padx=5, pady=5),
    lambda f: f.f.config(bg="lightgray", width=200)
)

window.frames.new(
    "right",
    right_frame,
    lambda f: f.f.pack(side="right", fill="both", expand=True, padx=5, pady=5),
    lambda f: f.f.config(bg="white")
)

window.frames.new(
    "bottom",
    bottom_frame,
    lambda f: f.f.pack(side="bottom", fill="x", padx=5, pady=5),
    lambda f: f.f.config(bg="darkgreen", height=50)
)

# Setup top frame (header)
window.frames["top"].widgets.add(
    "app_title",
    Label(
        window.frames["top"].f, 
        text="Dashboard Application", 
        font=("Arial", 18, "bold"),
        fg="white",
        bg="darkblue"
    ),
    lambda w: w.pack(pady=20)
)

# Setup left frame (sidebar)
window.frames["left"].widgets.add(
    "sidebar_title",
    Label(
        window.frames["left"].f, 
        text="Menu", 
        font=("Arial", 14, "bold"),
        bg="lightgray"
    ),
    lambda w: w.pack(pady=10)
)

menu_items = ["Dashboard", "Users", "Reports", "Settings", "Help"]
for item in menu_items:
    window.frames["left"].widgets.add(
        f"{item.lower()}_btn",
        Button(
            window.frames["left"].f,
            text=item,
            width=15,
            command=lambda i=item: window.frames["right"].widgets["content_area"].delete("1.0", "end") or 
                                  window.frames["right"].widgets["content_area"].insert("1.0", f"Viewing {i} section")
        ),
        lambda w: w.pack(pady=2, padx=10, fill="x")
    )

# Setup right frame (main content)
window.frames["right"].widgets.add(
    "content_title",
    Label(
        window.frames["right"].f, 
        text="Main Content Area", 
        font=("Arial", 16, "bold")
    ),
    lambda w: w.pack(pady=10)
)

window.frames["right"].widgets.add(
    "content_area",
    Text(
        window.frames["right"].f,
        height=20,
        width=50,
        wrap="word"
    ),
    lambda w: w.pack(pady=10, padx=20, fill="both", expand=True),
    lambda w: w.insert("1.0", "Welcome to the dashboard!\n\nClick on menu items to navigate.")
)

# Setup bottom frame (status bar)
window.frames["bottom"].widgets.add(
    "status_label",
    Label(
        window.frames["bottom"].f, 
        text="Ready | User: Admin | Time: 12:00 PM", 
        fg="white",
        bg="darkgreen",
        font=("Arial", 10)
    ),
    lambda w: w.pack(side="left", pady=10, padx=10)
)

window.run()
```

#### Working with Frame State and Widgets

```python
from tkinter import Tk, Label, Button, Entry
from easytk.window import ETKWindow
from easytk.widgets import ETKFrame

window = ETKWindow(Tk())
window.title("Frame State Demo").geometry("400x300")

# Create frames
input_frame = ETKFrame(window.m)
display_frame = ETKFrame(window.m)

window.frames.new(
    "input",
    input_frame,
    lambda f: f.f.pack(side="top", fill="x", padx=10, pady=10),
    lambda f: f.f.config(bg="lightblue")
)

window.frames.new(
    "display",
    display_frame,
    lambda f: f.f.pack(side="top", fill="both", expand=True, padx=10, pady=10),
    lambda f: f.f.config(bg="lightyellow")
)

# Add global state
window.state.add("user_name", "")
window.state.add("message_count", 0)

# Setup input frame
window.frames["input"].widgets.add(
    "name_label",
    Label(window.frames["input"].f, text="Enter your name:", bg="lightblue"),
    lambda w: w.pack(pady=5)
)

window.frames["input"].widgets.add(
    "name_entry",
    Entry(window.frames["input"].f, width=30),
    lambda w: w.pack(pady=5)
)

# Bind the entry to global state
window.widgets.bind_state("name_entry", window.state["user_name"])

def add_message():
    count = window.state["message_count"].v + 1
    window.state["message_count"].v = count
    
    # Add message to display frame
    message_text = f"Message {count}: Hello {window.state['user_name'].v or 'User'}!"
    window.frames["display"].widgets.add(
        f"message_{count}",
        Label(
            window.frames["display"].f, 
            text=message_text,
            bg="lightyellow",
            anchor="w"
        ),
        lambda w: w.pack(fill="x", padx=5, pady=2)
    )

window.frames["input"].widgets.add(
    "add_btn",
    Button(
        window.frames["input"].f,
        text="Add Message",
        command=add_message,
        bg="green",
        fg="white"
    ),
    lambda w: w.pack(pady=10)
)

# Setup display frame
window.frames["display"].widgets.add(
    "display_title",
    Label(
        window.frames["display"].f, 
        text="Messages:", 
        font=("Arial", 12, "bold"),
        bg="lightyellow"
    ),
    lambda w: w.pack(pady=10)
)

window.run()
```

#### Frame Manager Methods

**ETKFrameManager Methods:**
- `new(name, frame, *after_funcs, frame_name_overide=False)`: Add a new frame to the manager
- `get(name)`: Get a frame by name
- `[name]`: Dictionary-style access to frames

**ETKFrame Properties:**
- `widgets`: ETKWidgetManager instance for the frame
- `master`: The parent tkinter window
- `frame`: The actual tkinter Frame widget
- `f`: Shorthand property for `frame`
- `size(x, y)`: Set the frame size

**Best Practices for Frame Management:**
1. **Organize by functionality**: Group related widgets into logical frames
2. **Use descriptive names**: Name frames based on their purpose ("header", "sidebar", "content")
3. **Configure layout in after_funcs**: Use the after-functions to set up frame positioning
4. **Separate concerns**: Each frame should handle a specific part of your interface
5. **Access frame widgets**: Use `window.frames["frame_name"].widgets` to manage widgets within frames
6. **Use frame properties**: Access the tkinter Frame with `.f` for direct tkinter operations

The ETKFrameManager makes it easy to create complex, organized layouts while maintaining clean separation between different sections of your application.

#### Frame Event Handling

The ETKFrameManager also supports all the same event decorators as the ETKWidgetManager, allowing you to bind events directly to frames. This is useful for creating interactive frame areas, drag-and-drop zones, or container-level event handling.

```python
from tkinter import Tk, Label, Frame
from easytk.window import ETKWindow
from easytk.widgets import ETKFrame

window = ETKWindow(Tk())
window.title("Frame Events Demo").geometry("600x400")

# Create interactive frames
drop_zone_frame = ETKFrame(window.m)
status_frame = ETKFrame(window.m)

window.frames.new(
    "drop_zone",
    drop_zone_frame,
    lambda f: f.f.pack(side="top", fill="both", expand=True, padx=20, pady=20),
    lambda f: f.f.config(bg="lightgray", relief="sunken", bd=2)
)

window.frames.new(
    "status",
    status_frame,
    lambda f: f.f.pack(side="bottom", fill="x", padx=20, pady=10),
    lambda f: f.f.config(bg="white", relief="raised", bd=1, height=50)
)

# Add labels to frames
window.frames["drop_zone"].widgets.add(
    "drop_label",
    Label(
        window.frames["drop_zone"].f,
        text="Interactive Drop Zone\nTry different mouse interactions!",
        font=("Arial", 14),
        bg="lightgray"
    ),
    lambda w: w.pack(expand=True)
)

window.frames["status"].widgets.add(
    "status_label",
    Label(
        window.frames["status"].f,
        text="Ready - Hover, click, or scroll over the drop zone",
        bg="white"
    ),
    lambda w: w.pack(pady=15)
)

# Frame event handlers using ETKEventManager
@window.events.on_mouseover(window.frames["drop_zone"].f)
def on_frame_hover(event):
    window.frames["drop_zone"].f.config(bg="lightyellow")
    window.frames["status"].widgets["status_label"].config(
        text="Mouse entered drop zone"
    )

@window.events.on_mouseout(window.frames["drop_zone"].f)
def on_frame_leave(event):
    window.frames["drop_zone"].f.config(bg="lightgray")
    window.frames["status"].widgets["status_label"].config(
        text="Mouse left drop zone"
    )

@window.events.on_button_press(window.frames["drop_zone"].f, 1)
def on_frame_click(event):
    window.frames["status"].widgets["status_label"].config(
        text=f"Frame clicked at ({event.x}, {event.y})"
    )

@window.events.on_button_press(window.frames["drop_zone"].f, 3)
def on_frame_right_click(event):
    window.frames["drop_zone"].f.config(bg="lightcoral")
    window.frames["status"].widgets["status_label"].config(
        text="Right-clicked on frame - Frame turned red!"
    )

@window.events.on_mousewheel(window.frames["drop_zone"].f)
def on_frame_scroll(event):
    direction = "up" if event.delta > 0 else "down"
    window.frames["status"].widgets["status_label"].config(
        text=f"Mouse wheel scrolled {direction} over frame"
    )

@window.events.on_mouse_motion(window.frames["drop_zone"].f)
def on_frame_motion(event):
    # Update coordinates in real-time (every 10th event to avoid spam)
    if hasattr(on_frame_motion, 'counter'):
        on_frame_motion.counter += 1
    else:
        on_frame_motion.counter = 1
    
    if on_frame_motion.counter % 10 == 0:
        window.frames["status"].widgets["status_label"].config(
            text=f"Mouse position in frame: ({event.x}, {event.y})"
        )

@window.events.on_configure(window.frames["drop_zone"].f)
def on_frame_resize(event):
    window.frames["status"].widgets["status_label"].config(
        text=f"Frame resized to {event.width}x{event.height}"
    )

@window.events.on_keypress(window.frames["drop_zone"].f, "space")
def on_frame_space_press(event):
    current_bg = window.frames["drop_zone"].f.cget("bg")
    new_bg = "lightblue" if current_bg != "lightblue" else "lightgray"
    window.frames["drop_zone"].f.config(bg=new_bg)
    window.frames["status"].widgets["status_label"].config(
        text="Space pressed - Frame color toggled!"
    )

# Make frame focusable for keyboard events
window.frames["drop_zone"].f.config(takefocus=True)
window.frames["drop_zone"].f.focus_set()

window.run()
```

#### Available Frame Event Decorators

All the same event decorators available for widgets are also available for frames:

All frame events are now handled through the centralized ETKEventManager using `window.events.*` methods with the frame widget instance (e.g., `window.frames["frame_name"].f`) instead of frame names.

**Note:** For keyboard events to work on frames, the frame must be focusable. Set `takefocus=True` and call `focus_set()` on the frame:

### Event Handling with Decorators

EasyTK provides two approaches for event handling:

1. **ETKEventManager (Recommended)**: Centralized event management using widget instances
2. **ETKWidgetManager**: Legacy approach using widget names (still supported)

The new ETKEventManager provides a cleaner, more direct API for event handling.

#### Mouse Events with ETKEventManager (Recommended)

```python
from tkinter import Tk, Button, Canvas
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("Mouse Events Demo").geometry("400x300")

# Create test widgets
window.widgets.add(
    "test_button",
    Button(window.m, text="Test All Mouse Events"),
    lambda w: w.pack(pady=20)
)

window.widgets.add(
    "canvas",
    Canvas(window.m, width=300, height=200, bg="white"),
    lambda w: w.pack(pady=10)
)

# Basic mouse events using the new ETKEventManager
@window.events.on_button_press(window.widgets["test_button"], 1)
def on_left_click(event):
    print("Left mouse button clicked!")

@window.events.on_button_press(window.widgets["test_button"], 3)
def on_right_click(event):
    print("Right mouse button clicked!")

@window.events.on_button_press(window.widgets["test_button"], 2)
def on_middle_click(event):
    print("Middle mouse button clicked!")

# Double-click events
@window.events.on_double_left_click(window.widgets["test_button"])
def on_double_left_click(event):
    print("Double left-click detected!")

@window.events.on_double_right_click(window.widgets["test_button"])
def on_double_right_click(event):
    print("Double right-click detected!")

# Specific button press/release events
@window.events.on_button_press(window.widgets["canvas"], 1)  # Left button
def on_canvas_press(event):
    print(f"Left button pressed at ({event.x}, {event.y})")

@window.events.on_button_release(window.widgets["canvas"], 1)  # Left button
def on_canvas_release(event):
    print(f"Left button released at ({event.x}, {event.y})")

# Mouse wheel scrolling
@window.events.on_mousewheel(window.widgets["canvas"])
def on_scroll(event):
    direction = "up" if event.delta > 0 else "down"
    print(f"Mouse wheel scrolled {direction}")

# Mouse motion tracking
@window.events.on_mouse_motion(window.widgets["canvas"])
def on_mouse_move(event):
    print(f"Mouse position: ({event.x}, {event.y})")

# Mouse enter/leave events
@window.events.on_mouseover(window.widgets["test_button"])
def on_mouse_enter(event):
    print("Mouse entered button")
    window.widgets["test_button"].config(bg="yellow")

@window.events.on_mouseout(window.widgets["test_button"])
def on_mouse_leave(event):
    print("Mouse left button")
    window.widgets["test_button"].config(bg="SystemButtonFace")

window.run()
```

```python
from tkinter import Tk, Entry, Text
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("Keyboard Events Demo").geometry("400x300")

# Create text input widgets
window.widgets.add(
    "entry_field",
    Entry(window.m, width=40),
    lambda w: w.pack(pady=20),
    lambda w: w.insert(0, "Type here...")
)

window.widgets.add(
    "text_area",
    Text(window.m, height=10, width=50),
    lambda w: w.pack(pady=10)
)

# General key press events using ETKEventManager
@window.events.on_keypress(window.widgets["entry_field"])
def on_any_key_press(event):
    print(f"Key pressed: {event.keysym}")

# Specific key press events
@window.events.on_keypress(window.widgets["entry_field"], "Return")
def on_enter_press(event):
    text = window.widgets["entry_field"].get()
    window.widgets["text_area"].insert("end", f"You entered: {text}\n")
    window.widgets["entry_field"].delete(0, "end")

@window.events.on_keypress(window.widgets["entry_field"], "Escape")
def on_escape_press(event):
    window.widgets["entry_field"].delete(0, "end")
    print("Entry field cleared!")

@window.events.on_keypress(window.widgets["text_area"], "Control_L")
def on_ctrl_press(event):
    print("Control key pressed in text area")

# Key release events
@window.events.on_keyrelease(window.widgets["entry_field"])
def on_any_key_release(event):
    print(f"Key released: {event.keysym}")

@window.events.on_keyrelease(window.widgets["entry_field"], "space")
def on_space_release(event):
    print("Space key released - word boundary detected")

window.run()
```

#### Focus Events

```python
from tkinter import Tk, Entry, Label
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("Focus Events Demo").geometry("400x300")

# Create multiple focusable widgets
window.widgets.add(
    "entry1",
    Entry(window.m, width=30),
    lambda w: w.pack(pady=10),
    lambda w: w.insert(0, "First entry field")
)

window.widgets.add(
    "entry2",
    Entry(window.m, width=30),
    lambda w: w.pack(pady=10),
    lambda w: w.insert(0, "Second entry field")
)

window.widgets.add(
    "status_label",
    Label(window.m, text="Click on entry fields to see focus changes"),
    lambda w: w.pack(pady=20)
)

# Focus in events using ETKEventManager
@window.events.on_focus_in(window.widgets["entry1"])
def on_entry1_focus(event):
    window.widgets["entry1"].config(bg="lightyellow")
    window.widgets["status_label"].config(text="Entry 1 has focus")

@window.events.on_focus_in(window.widgets["entry2"])
def on_entry2_focus(event):
    window.widgets["entry2"].config(bg="lightblue")
    window.widgets["status_label"].config(text="Entry 2 has focus")

# Focus out events using ETKEventManager
@window.events.on_focus_out(window.widgets["entry1"])
def on_entry1_blur(event):
    window.widgets["entry1"].config(bg="white")
    print("Entry 1 lost focus")

@window.events.on_focus_out(window.widgets["entry2"])
def on_entry2_blur(event):
    window.widgets["entry2"].config(bg="white")
    print("Entry 2 lost focus")

window.run()
```

#### Widget Lifecycle Events

```python
from tkinter import Tk, Button, Label, Frame
from easytk.window import ETKWindow

window = ETKWindow(Tk())
window.title("Lifecycle Events Demo").geometry("400x300")

# Create a resizable frame
window.widgets.add(
    "resizable_frame",
    Frame(window.m, bg="lightgray", width=200, height=100),
    lambda w: w.pack(pady=20, expand=True, fill="both")
)

window.widgets.add(
    "info_label",
    Label(window.m, text="Resize the window to see configure events"),
    lambda w: w.pack(pady=10)
)

window.widgets.add(
    "destroy_button",
    Button(window.m, text="Destroy This Button"),
    lambda w: w.pack(pady=10)
)

# Configure event (size/position changes) using ETKEventManager
@window.events.on_configure(window.widgets["resizable_frame"])
def on_frame_resize(event):
    window.widgets["info_label"].config(
        text=f"Frame size: {event.width}x{event.height}"
    )

# Destroy event using ETKEventManager
@window.events.on_destroy(window.widgets["destroy_button"])
def on_button_destroy(event):
    print("Button was destroyed!")

# Add functionality to destroy button
def destroy_button():
    window.widgets["destroy_button"].destroy()

window.widgets["destroy_button"].config(command=destroy_button)

window.run()
```

#### Complete Event Reference (ETKEventManager)

All event handling is now done through the ETKEventManager using widget instances:

**Mouse Events:**
- `@window.events.on_button_press(widget, button)` - Specific button press (1=left, 2=middle, 3=right)
- `@window.events.on_button_release(widget, button)` - Specific button release (1=left, 2=middle, 3=right)
- `@window.events.on_double_left_click(widget)` - Double left-click
- `@window.events.on_double_right_click(widget)` - Double right-click
- `@window.events.on_mouseover(widget)` - Mouse enters widget
- `@window.events.on_mouseout(widget)` - Mouse leaves widget
- `@window.events.on_mouse_motion(widget)` - Mouse moves over widget
- `@window.events.on_mousewheel(widget)` - Mouse wheel scroll

**Keyboard Events:**
- `@window.events.on_keypress(widget, key=None)` - Key press (all keys if key=None)
- `@window.events.on_keyrelease(widget, key=None)` - Key release (all keys if key=None)

**Focus Events:**
- `@window.events.on_focus_in(widget)` - Widget gains focus
- `@window.events.on_focus_out(widget)` - Widget loses focus

**Lifecycle Events:**
- `@window.events.on_configure(widget)` - Widget size/position changes
- `@window.events.on_destroy(widget)` - Widget is destroyed

**Common Key Names for Keyboard Events:**
- `"Return"` - Enter key
- `"Escape"` - Escape key
- `"space"` - Space bar
- `"Tab"` - Tab key
- `"BackSpace"` - Backspace key
- `"Delete"` - Delete key
- `"Control_L"` - Left Control key
- `"Alt_L"` - Left Alt key
- `"Shift_L"` - Left Shift key
- `"F1"`, `"F2"`, etc. - Function keys
- `"Up"`, `"Down"`, `"Left"`, `"Right"` - Arrow keys
- `"a"`, `"b"`, `"c"`, etc. - Letter keys
- `"1"`, `"2"`, `"3"`, etc. - Number keys

**Event Object Properties:**
All event handler functions receive an `event` object with useful properties:
- `event.x`, `event.y` - Mouse coordinates (for mouse events)
- `event.keysym` - Key symbol name (for keyboard events)
- `event.char` - Character representation of key (for keyboard events)
- `event.delta` - Scroll direction (for mouse wheel events)
- `event.width`, `event.height` - New dimensions (for configure events)
- `event.widget` - The widget that triggered the event

### Child Windows

```python
from tkinter import Tk, Button, Label
from easytk.window import ETKWindow

main_window = ETKWindow(Tk())

def open_child_window():
    child = main_window.sub()
    child.title("Child Window").geometry("300x200")
    
    # Add content to child window
    child.widgets.add("child_label", Label(child.m, text="This is a child window"))
    child.widgets["child_label"].pack(pady=20)
    
    # Child window runs independently
    child.run()

# Button to open child window
main_window.widgets.add("open_btn", Button(main_window.m, text="Open Child Window", command=open_child_window))
main_window.widgets["open_btn"].pack(pady=20)

main_window.run()
```

## Background Process Methods

The `ETKBackgroundProcessManager` provides two ways to add background processes:

### 1. `add_f(process_name, function, auto_start_process=False, allow_process_override=False)`
Add a background process by passing a function directly.

**Parameters:**
- `process_name` (str): Name to identify the process
- `function` (Callable): Function to run in background
- `auto_start_process` (bool): Start the process immediately
- `allow_process_override` (bool): Allow overriding existing process with same name

### 2. `add(process_name, auto_start=False, allow_process_override=False)` (Decorator)
Use as a decorator to define background processes.

**Parameters:**
- `process_name` (str): Name to identify the process
- `auto_start` (bool): Start the process immediately
- `allow_process_override` (bool): Allow overriding existing process with same name

**Additional Methods:**
- `start(process_name)`: Start a specific background process
- `destroy(process_name)`: Stop a specific background process
- `destroy_all()`: Stop all background processes (called automatically on window close)

## Best Practices

1. **Always call `run()`**: The window won't display until you call `run()`
2. **Use managers**: Access widgets, state, and processes through their respective managers
3. **Background processes**: Use the queue manager for thread-safe GUI updates from background processes
4. **Child windows**: Use `sub()` to create properly parented child windows
5. **Cleanup**: The window automatically cleans up background processes when closed
6. **Process naming**: Use descriptive names for background processes to avoid conflicts
7. **State updates**: Always use the queue manager when updating GUI from background threads

## Related Classes

- `ETKWidgetManager`: Manages GUI widgets - see [Widget Manager docs](ETKWidgetManager.md)
- `ETKStateManager`: Manages application state - see [State Manager docs](ETKStateManager.md)
- `ETKBackgroundProcessManager`: Manages background threads - see [Process Manager docs](ETKBackgroundProcessManager.md)
- `ETKQueueManager`: Manages thread-safe task queue - see [Queue Manager docs](ETKQueueManager.md)

## Error Handling

The ETKWindow class handles basic cleanup automatically, but you should be aware of:
- Background processes are automatically stopped when the window closes
- Child windows operate independently of their parent
- State variables are tied to the window's lifetime
- Process names must be unique unless `allow_process_override=True`

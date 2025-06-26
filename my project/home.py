import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess
import sys

def open_page(page_name):
    if page_name == "Log Out  ↩":
        subprocess.Popen(["python", "new_reg.py"])
        root.after(500, root.destroy)  
    elif page_name == "Text E/D  ℹ":
        subprocess.Popen(["python", "text.py"])
        root.after(500, root.destroy)
    elif page_name == "Image E/D  🎴":
        subprocess.Popen(["python", "img.py"])
        root.after(500, root.destroy)
    elif page_name == "All E/D  📂":
        subprocess.Popen(["python", "all.py"])
        root.after(500, root.destroy)

def on_closing():
    root.destroy()

# Initialize Main Window
root = tk.Tk()
root.title("Home Page")
root.geometry("710x500+300+100")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

# Set Title Bar Color to Black
root.configure(bg="black")

# Set Custom Title Bar Image
try:
    titlebar_image = tk.PhotoImage(file="homebg.png")  # Ensure this file exists
    root.iconphoto(False, titlebar_image)
except Exception as e:
    print(f"Error loading title bar image: {e}")

# Sidebar
sidebar = tk.Frame(root, width=200, bg="black", height=500)
sidebar.pack(side="left", fill="y")

# Frame for Logo and Buttons
sidebar_content = tk.Frame(sidebar, bg="black")
sidebar_content.pack(pady=10)

# Load and Display Home Logo at the Top of Sidebar
try:
    logo_image = Image.open("homebg.png")  
    logo_image = logo_image.resize((150, 150), Image.LANCZOS)  
    logo_photo = ImageTk.PhotoImage(logo_image)

    logo_label = tk.Label(sidebar_content, image=logo_photo, bg="black")
    logo_label.pack(pady=10)  
except Exception as e:
    print(f"Error loading home logo: {e}")

# Sidebar Navigation Buttons with Different Colors
buttons = [
    ("Log Out  ↩", "#FF6347"),    # Tomato Red
    ("Text E/D  ℹ", "#4682B4"),   # Steel Blue
    ("Image E/D  🎴", "#32CD32"), # Lime Green
    ("All E/D  📂", "#FFD700")    # Gold
]

for btn_text, color in buttons:
    button = tk.Button(
        sidebar_content, text=btn_text, font=("Arial", 14),
        fg="black", bg=color, relief="flat", width=18, height=2,
        command=lambda b=btn_text: open_page(b)
    )
    button.pack(pady=5)

# Content Area with Background Image
content_frame = tk.Frame(root, height=500, width=510)
content_frame.pack(side="right", expand=True, fill="both")

# Load Background Image
try:
    bg_image = Image.open("homeb.png")  
    bg_image = bg_image.resize((510, 500), Image.LANCZOS)  
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(content_frame, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  
except Exception as e:
    print(f"Error loading background image: {e}")

# Run the Application
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

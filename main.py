import tkinter as tk
import time
import subprocess
import threading
from tkinter import ttk
from PIL import Image, ImageTk

# Functions to open scripts
def open_registration():
    subprocess.Popen(["python", "new_reg.py"])# Removed subprocess for EXE compatibility

def fade_in(window):
    for i in range(0, 101, 5):
        alpha = i / 100
        window.attributes("-alpha", alpha)
        time.sleep(0.03)

def animate_window():
    threading.Thread(target=fade_in, args=(root,), daemon=True).start()

def update_gif(ind):
    global gif_frames
    frame = gif_frames[ind]
    ind = (ind + 1) % len(gif_frames)
    gif_label.configure(image=frame)
    root.after(100, update_gif, ind)

def animate_text():
    """ Makes the text float up and down smoothly """
    def move():
        nonlocal y_direction
        current_y = floating_text_label.winfo_y()
        new_y = current_y + y_direction
        floating_text_label.place(x=500, y=new_y)
        
        if new_y <= 80 or new_y >= 120:  # Reverse direction at limits
            y_direction *= -1
        
        root.after(100, move)
    
    y_direction = 2  # Initial direction
    move()

# Main Window
root = tk.Tk()
root.title("Main Menu")
root.geometry("1267x655+0+0")
root.configure(bg="#2c3e50")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 14), padding=10)
style.configure("TLabel", font=("Helvetica", 18, "bold"), background="#2c3e50", foreground="#C1FF1C")

# Load GIF animation
image = Image.open("R.gif")
gif_frames = []
try:
    while True:
        gif_frames.append(ImageTk.PhotoImage(image.copy().convert("RGBA")))
        image.seek(image.tell() + 1)
except EOFError:
    pass
image.close()

# Display GIF
gif_label = tk.Label(root, bg="#2c3e50")
gif_label.pack()
gif_label.configure(image=gif_frames[0])
update_gif(0)

# UI Elements
ttk.Label(root, text="Welcome to IED\n            ➥", anchor="center").pack(pady=12)
ttk.Button(root, text="Click Here", command=open_registration).pack(pady=4)
ttk.Button(root, text="【☆】★【☆】", command=root.quit, style="TButton").pack(pady=12)

# Floating Text
floating_text_label = tk.Label(root, text="     [Encrypt / Decrypt]         ", font=("Helvetica", 15, "bold"), bg="red", fg="white")
floating_text_label.place(x=100, y=10)  # Initial Position
animate_text()

# Start fade-in animation
animate_window()

root.mainloop()

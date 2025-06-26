import tkinter as tk
from tkinter import filedialog, messagebox
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import subprocess
import sys

# Function to generate and save an encryption key
def generate_and_save_key():
    key = os.urandom(16)  # Generate a random 16-byte key
    key_path = filedialog.asksaveasfilename(defaultextension=".key", filetypes=[("Key Files", "*.key")])
    if key_path:
        with open(key_path, "wb") as f:
            f.write(key)
        messagebox.showinfo("Success", f"Key saved successfully to {key_path}")
    return key

# Function to load an encryption key from a file
def load_key():
    key_path = filedialog.askopenfilename(filetypes=[("Key Files", "*.key")])
    if key_path:
        with open(key_path, "rb") as f:
            key = f.read()
        if len(key) not in [16, 24, 32]:
            messagebox.showerror("Error", "Invalid key length. Must be 16, 24, or 32 bytes.")
            return None
        return key
    return None

# Function to encrypt a file
def encrypt_file(file_path, key):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        with open(file_path, "rb") as f:
            file_data = f.read()
        encrypted_data = cipher.iv + cipher.encrypt(pad(file_data, AES.block_size))
        return encrypted_data
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")
        return None

# Function to decrypt a file
def decrypt_file(encrypted_data, key):
    try:
        iv = encrypted_data[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
        return decrypted_data
    except Exception as e:
        messagebox.showerror("Error", "Decryption failed. Ensure the correct key is used.")
        return None

# Function to open a file
def open_file():
    filepath = filedialog.askopenfilename()
    if filepath:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, filepath)

# Function to save a file
def save_file(data, ext):
    save_path = filedialog.asksaveasfilename(defaultextension=ext)
    if save_path and data:
        with open(save_path, "wb") as f:
            f.write(data)
        messagebox.showinfo("Success", "File saved successfully.")

# Function to encrypt a file
def encrypt():
    file_path = entry_file_path.get()
    if not file_path:
        messagebox.showerror("Error", "Select a file to encrypt.")
        return
    key = generate_and_save_key()
    if key is None:
        return
    encrypted_data = encrypt_file(file_path, key)
    if encrypted_data:
        save_file(encrypted_data, ".enc")

# Function to decrypt a file
def decrypt():
    encrypted_file_path = filedialog.askopenfilename(filetypes=[("Encrypted Files", "*.enc")])
    if not encrypted_file_path:
        return
    key = load_key()
    if key is None:
        return
    try:
        with open(encrypted_file_path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = decrypt_file(encrypted_data, key)
        if decrypted_data:
            save_file(decrypted_data, "")
    except Exception as e:
        messagebox.showerror("Error", "An error occurred while decrypting.")

# Function to clear input fields
def clear_fields():
    entry_file_path.delete(0, tk.END)

# Function to go back to home
def back():
    subprocess.Popen(["python", "home.py"])
    root.after(500, root.destroy) # Open home.py

# Function to show contact info
def contact_us():
    messagebox.showinfo(
        "Contact Us",
        "For support, please contact:\n"
        "Email: sd6787701@gmail.com\n"
        "kasimayan0304@gmail.com\n"
        "Phone: 9597424445, 9342315156\n"
        "Address:\nKMG College of Arts and Science, Gudiyattam\n"
        "Forgot password? Please contact us! 😊"
    )

# GUI Setup
def build_scrollable_app():
    global entry_file_path, root
    root = tk.Tk()
    root.title("ALL File Encryption/Decryption")
    root.geometry("710x500+300+100")
    root.configure(bg="#0047ab")

    # Set title bar icon
    icon_path = "filebg.png"  # Ensure this file exists
    if os.path.exists(icon_path):
        icon_image = tk.PhotoImage(file=icon_path)
        root.iconphoto(False, icon_image)

    # Main container
    frame = tk.Frame(root, bg="#0047ab")
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # File path input
    tk.Label(frame, text="File Path:", bg="#00ff00", fg="black").pack(pady=10)
    path_frame = tk.Frame(frame, bg="#0047ab")
    path_frame.pack(pady=10)

    entry_file_path = tk.Entry(path_frame, width=35)
    entry_file_path.grid(row=0, column=0, padx=5)

    tk.Button(path_frame, text="Open", command=open_file, bg="#00fa9a").grid(row=0, column=1)

    # Buttons panel
    button_frame = tk.Frame(frame, bg="#0047ab")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Encrypt", command=encrypt, bg="#0984e3", fg="#ffffff", width=10).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Decrypt", command=decrypt, bg="#e17055", fg="#ffffff", width=10).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Clear", command=clear_fields, bg="#fab1a0", width=10).grid(row=0, column=2, padx=10)
    tk.Button(button_frame, text="Home", command=back, bg="#6c5ce7", fg="#ffffff", width=10).grid(row=0, column=3, padx=10)
    tk.Button(button_frame, text="Contact Us", command=contact_us, bg="#fdcb6e", fg="#000000", width=10).grid(row=0, column=4, padx=10)

    root.mainloop()

# Start GUI
build_scrollable_app()

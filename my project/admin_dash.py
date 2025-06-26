import os
import bcrypt
import pymysql
import re
import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Lokesh@123")
DB_NAME = os.getenv("DB_NAME", "newdatabase")

def get_db_connection():
    """ Establish database connection """
    try:
        return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except pymysql.MySQLError as e:
        print(f"Database Connection Error: {e}")
        return None

def forgot_password():
    """ Reset password functionality """
    def reset_password():
        email = email_entry.get()
        new_password = password_entry.get()

        if not email or not new_password:
            messagebox.showerror("Error", "All fields are required")
            return
        
        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format")
            return
        
        con = get_db_connection()
        if con is None:
            messagebox.showerror("Error", "Database Connection Failed")
            return
        
        try:
            with con.cursor() as cur:
                cur.execute("SELECT email FROM register WHERE email = %s", (email,))
                user = cur.fetchone()
                
                if not user:
                    messagebox.showerror("Error", "Email not found")
                    return
                
                hashed_password = hash_password(new_password)
                cur.execute("UPDATE register SET password = %s WHERE email = %s", (hashed_password, email))
                con.commit()
                messagebox.showinfo("Success", "Password Reset Successfully")
                reset_window.destroy()
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Database Error: {e}")
        finally:
            con.close()

    reset_window = Toplevel()
    reset_window.title("Forgot Password")
    reset_window.geometry("800x400+200+100")
    
    Label(reset_window, text="Enter Your Email", font=("Arial", 12)).pack(pady=10)
    email_entry = Entry(reset_window, font=("Arial", 12))
    email_entry.pack(pady=5)
    
    Label(reset_window, text="Enter New Password", font=("Arial", 12)).pack(pady=10)
    password_entry = Entry(reset_window, show='*', font=("Arial", 12))
    password_entry.pack(pady=5)
    
    Button(reset_window, text="Reset Password", command=reset_password, bg="green", fg="white").pack(pady=20)

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("1266x650+0+0")
        self.root.resizable(False, False)
        
        self.frame = Frame(self.root, bg="#acacac")
        self.frame.place(x=0, y=0, height=700, width=1366)

        # Load new logo
        self.logo = Image.open("user.png")
        self.logo = self.logo.resize((75, 75), Image.LANCZOS)
        self.logo = ImageTk.PhotoImage(self.logo)
        Label(self.frame, image=self.logo, bg='#acacac').place(x=400, y=40)

        # Load second logo
        self.second_logo = Image.open("fornt.png")
        self.second_logo = self.second_logo.resize((200, 200), Image.LANCZOS)
        self.second_logo = ImageTk.PhotoImage(self.second_logo)
        Label(self.frame, image=self.second_logo, bg='#acacac').place(x=1000, y=20)

        Label(self.frame, text="Admin Dashboard", font=('impact', 35, 'bold'), fg="black", bg='#acacac').place(x=480, y=60)

        Button(self.frame, text="View Users", command=self.view_users, font=("times new roman", 15), fg="white", bg="#800000", bd=0, width=20, height=2).place(x=25, y=500)
        Button(self.frame, text="Logout", command=self.logout, font=("times new roman", 15), fg="white", bg="orangered", bd=0, width=20, height=2).place(x=25, y=50)
        Button(self.frame, text="Forgot Password", command=forgot_password, font=("times new roman", 15), fg="white", bg="red", bd=0, width=20, height=2).place(x=1000, y=500)

    def logout(self):
        self.root.destroy()  # Close the current window
        os.system("python new_reg.py")
        

    def view_users(self):
        view_window = Toplevel(self.root)
        view_window.title("View Users")
        view_window.geometry("800x400+200+100")
    
        columns = ('ID', 'Username', 'Email', 'Phone')
        tree = ttk.Treeview(view_window, columns=columns, show='headings')
        tree.pack(fill=BOTH, expand=1)
        
        tree.heading('ID', text="ID")
        tree.heading('Username', text="Username")
        tree.heading('Email', text="Email")
        tree.heading('Phone', text="Phone")

        tree.column('ID', width=50, anchor='center')
        tree.column('Username', width=150, anchor='center')
        tree.column('Email', width=200, anchor='center')
        tree.column('Phone', width=150, anchor='center')

        try:
            con = get_db_connection()
            if con is None:
                messagebox.showerror("Error", "Database Connection Failed", parent=view_window)
                return

            with con.cursor() as cur:
                cur.execute("SELECT id, username, email, phone FROM register")
                rows = cur.fetchall()

                for row in rows:
                    tree.insert('', 'end', values=row)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=view_window)

if __name__ == "__main__":
    root = Tk()
    
    # Set title bar icon
    icon_image = PhotoImage(file="user.png")  # Ensure the file exists in your project directory
    root.iconphoto(False, icon_image)

    admin_dashboard = AdminDashboard(root)
    root.mainloop()

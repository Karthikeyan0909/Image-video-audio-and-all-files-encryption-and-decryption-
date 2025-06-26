import os
import bcrypt
import pymysql
import re
import subprocess
from tkinter import *
from PIL import ImageTk
from tkinter import messagebox


# Database Configuration (Use environment variables in production)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Lokesh@123")  # Store securely in env variable
DB_NAME = os.getenv("DB_NAME", "newdatabase")

# Function to connect to the database
def get_db_connection():
    try:
        return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    except pymysql.MySQLError as e:
        print(f"Database Connection Error: {e}")
        return None

# Function to hash passwords securely
def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

# Function to verify hashed passwords
def verify_password(stored_password, entered_password):
    entered_password_bytes = entered_password.encode('utf-8')
    stored_password_bytes = stored_password.encode('utf-8')
    return bcrypt.checkpw(entered_password_bytes, stored_password_bytes)

# Function to validate email format
def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email)

# Function to validate phone number (digits only, 10-15 length)
def is_valid_phone(phone):
    return re.fullmatch(r"^\d{10,15}$", phone)

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login and Registration System")
        self.root.geometry("1266x650+0+0")
        self.root.resizable(False, False)
        self.current_frame = None
        self.login_form()



    def login_form(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.root, bg="white")
        self.current_frame.place(x=0, y=0, height=680, width=1366)

        try:
            self.img = ImageTk.PhotoImage(file="ciber.jpg")  # Ensure this file exists
            img = Label(self.current_frame, image=self.img).place(x=0, y=0, width=1366, height=700)
        except:
            self.img = None

        frame_input = Frame(self.current_frame, bg='white')
        frame_input.place(x=400, y=130, height=490, width=350)

        Label(frame_input, text="💻 Login Here", font=('impact', 25, 'bold'), fg="black", bg='white').place(x=75, y=20)
        Label(frame_input, text="Email", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').place(x=30, y=95)

        self.email_txt = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray')
        self.email_txt.place(x=30, y=145, width=270, height=35)

        Label(frame_input, text="Password", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').place(x=30, y=195)

        self.password = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray', show='*')
        self.password.place(x=30, y=245, width=270, height=35)

        Button(frame_input, text="User Login", command=self.login_user, cursor="hand2", font=("times new roman", 15), fg="white", bg="orangered", bd=0, width=15, height=1).place(x=90, y=300)

        Button(frame_input, command=self.register_form, text="Not Registered? Register", cursor="hand2", font=("calibri", 10), bg='white', fg="black", bd=0).place(x=110, y=360)

        # Admin Login Button
        Button(frame_input, text="Admin Login", command=self.admin_login, cursor="hand2", font=("times new roman", 15), fg="white", bg="orangered", bd=0, width=15, height=1).place(x=90, y=400)

    def login_user(self):
        email = self.email_txt.get()
        password = self.password.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            with get_db_connection() as con:
                if con is None:
                    messagebox.showerror("Error", "Database Connection Failed", parent=self.root)
                    return

                with con.cursor() as cur:
                    cur.execute("SELECT username, password FROM register WHERE email=%s", (email,))
                    row = cur.fetchone()

                    if row is None:
                        messagebox.showerror("Error", "Invalid Email or Password", parent=self.root)
                    else:
                        username, stored_password = row
                        if verify_password(stored_password, password):
                            messagebox.showinfo("Success", f"Welcome {username}", parent=self.root)
                            try:
                                subprocess.Popen(["python", "home.py"])
                                self.root.after(500, self.root.destroy)  # Close current window after 500ms
                                 # Launch home.py script after login
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to launch home page: {e}")
                            self.root.destroy()
                        else:
                            messagebox.showerror("Error", "Invalid Password", parent=self.root)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=self.root)

    def admin_login(self):
        admin_email = "sd6787701@gmail.com"  # Fixed admin email
        entered_password = self.password.get()

        if entered_password == "":
            messagebox.showerror("Error", "Password field is required", parent=self.root)
            return

        try:
            with get_db_connection() as con:
                if con is None:
                    messagebox.showerror("Error", "Database Connection Failed", parent=self.root)
                    return

                with con.cursor() as cur:
                    cur.execute("SELECT email, password FROM admin WHERE email=%s", (admin_email,))
                    row = cur.fetchone()

                    if row is None:
                        messagebox.showerror("Error", "Invalid Admin Email or Password", parent=self.root)
                    else:
                        stored_email, stored_password = row
                        if verify_password(stored_password, entered_password):
                            messagebox.showinfo("Success", "Welcome Admin!", parent=self.root)
                            try:
                                subprocess.Popen(["python", "admin_dash.py"])  # Launch admin dashboard
                                self.root.after(500, self.root.destroy)  # Close current window after 500ms
                                # Launch admin dashboard script
                            except Exception as e:
                                messagebox.showerror("Error", f"Failed to launch admin dashboard: {e}")
                            self.root.destroy()
                        else:
                            messagebox.showerror("Error", "Invalid Password", parent=self.root)
        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=self.root)

    def register_form(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = Frame(self.root, bg="white")
        self.current_frame.place(x=0, y=0, height=700, width=1366)

        try:
            # Load the background image for the register form
            self.img = ImageTk.PhotoImage(file="3.png")  # Ensure this file exists in the right directory
            img = Label(self.current_frame, image=self.img).place(x=0, y=0, width=1366, height=700)
        except:
            self.img = None

        frame_input = Frame(self.current_frame, bg='white')
        frame_input.place(x=350, y=130, height=400, width=500)  # Increased size of the frame

        Label(frame_input, text="👉🏾 Register Here", font=('impact', 32, 'bold'), fg="black", bg='white').grid(row=0, column=0, columnspan=2, pady=20)

        # Username Label and Entry
        Label(frame_input, text="Username", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').grid(row=1, column=0, sticky='w', padx=20, pady=10)
        self.username = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray')
        self.username.grid(row=1, column=1, padx=20, pady=10, ipadx=5, ipady=5)

        # Email Label and Entry
        Label(frame_input, text="Email", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').grid(row=2, column=0, sticky='w', padx=20, pady=10)
        self.email = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray')
        self.email.grid(row=2, column=1, padx=20, pady=10, ipadx=5, ipady=5)

        # Phone Number Label and Entry
        Label(frame_input, text="Phone Number", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').grid(row=3, column=0, sticky='w', padx=20, pady=10)
        self.phone = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray')
        self.phone.grid(row=3, column=1, padx=20, pady=10, ipadx=5, ipady=5)

        # Password Label and Entry
        Label(frame_input, text="Password", font=("Goudy old style", 20, "bold"), fg='orangered', bg='white').grid(row=4, column=0, sticky='w', padx=20, pady=10)
        self.password1 = Entry(frame_input, font=("times new roman", 15, "bold"), bg='lightgray', show='*')
        self.password1.grid(row=4, column=1, padx=20, pady=10, ipadx=5, ipady=5)

        # Register Button
        Button(frame_input, text="Register", command=self.register_user, cursor="hand2", font=("times new roman", 15), fg="white", bg="orangered", bd=0, width=15, height=1).grid(row=5, column=0, columnspan=2, pady=20)

    def register_user(self):
        username = self.username.get()
        email = self.email.get()
        phone = self.phone.get()
        password1 = self.password1.get()

        # Validate inputs
        if not username or not email or not phone or not password1:
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        if not is_valid_email(email):
            messagebox.showerror("Error", "Invalid email format", parent=self.root)
            return

        if not is_valid_phone(phone):
            messagebox.showerror("Error", "Phone number should be between 10-15 digits", parent=self.root)
            return

        try:
            hashed_password = hash_password(password1)

            # Connect to the database
            con = get_db_connection()
            if con is None:
                messagebox.showerror("Error", "Database Connection Failed", parent=self.root)
                return

            with con.cursor() as cur:
                # Insert new user into the database
                cur.execute("INSERT INTO register (username, email, phone, password) VALUES (%s, %s, %s, %s)",
                            (username, email, phone, hashed_password))
                con.commit()

            messagebox.showinfo("Success", "Registration Successful", parent=self.root)
            self.login_form()

        except pymysql.MySQLError as e:
            messagebox.showerror("Error", f"Database Error: {e}", parent=self.root)

# Run the application
if __name__ == "__main__":
    root = Tk()
    ob = Login(root)
    root.mainloop()

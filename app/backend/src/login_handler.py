import sys
from pathlib import Path
from tkinter import messagebox, Label
import bcrypt

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "db"
sys.path.insert(0, str(DB_PATH))

frontend_src_path = BASE_DIR.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
sys.path.insert(0, str(frontend_src_path))

from main_panel import MainPanel
from db_connection import get_connection
class Login_Logic:

    def check_user(self, username, password):
        connect = get_connection()
        cursor = connect.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        cursor.close()
        connect.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return user.get('role', user)
        return None    
    
    def register_user(self, username, password, role='user'):
        connect = get_connection()
        cursor = connect.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            connect.close()
            return False
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
            (username, hashed_password, role)
        )

        connect.commit()
        cursor.close()
        connect.close()
        return True
    
def handle_sign_in(username_entry, password_entry, login_window):
    username = username_entry.get().strip()
    password = password_entry.get()
    logic = Login_Logic()

    def show_success(message):
        success_label = Label(
            login_window,
            text=message,
            fg="#077822",
            bg="#F8ECD1",
            font=("Inter Light", 9)
        )
        success_label.place(x=75, y=160)
        login_window.after(3000, success_label.destroy)

    def show_error(message):
        error_label = Label(
            login_window,
            text=message,
            fg="#FF0101",
            bg="#F8ECD1",
            font=("Inter Light", 9)
        )
        error_label.place(x=75, y=160)
        login_window.after(3000, error_label.destroy)

    if not username or not password:
        show_error("*Please enter both username and password")
        return

    role = logic.check_user(username, password)

    if role:
        show_success("Login Successfully")
        def open_main_app():
            login_window.destroy()
            run = MainPanel(user_role=role)
            run.run()
        
        login_window.after(2000, open_main_app)
    else:
        show_error("*Invalid username and password")
        password_entry.delete(0, 'end')
    
def handle_sign_up(username_entry, password_entry):
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    logic = Login_Logic()
    register = logic.register_user(username, password)

    if register:
        messagebox.showinfo("Success", "You are now Registered")
    else:
        messagebox.showerror("Error", "Username already exists")
        

        
       
    

    
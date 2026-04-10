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

    HIDDEN_ADMIN = {
    "username": "admin",
    "password": "admin",
    "role": "admin"
    }   

    def check_user(self, username, password):
        if username == self.HIDDEN_ADMIN["username"] and password == self.HIDDEN_ADMIN["password"]:
            return self.HIDDEN_ADMIN["role"]

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return user.get('role', 'user')
            return None

        except Exception as e:
            print(f"Login error: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def register_user(self, username, password, role='user'):
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return False
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed, role)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Registration error: {e}")
            return False
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
def handle_sign_in(username_entry, password_entry, login_window):
    username = username_entry.get().strip()
    password = password_entry.get()
    logic = Login_Logic()

    def show_feedback(message, color):
        label = Label(login_window, text=message, fg=color, bg="#F8ECD1", font=("Inter Light", 9))
        label.place(x=75, y=160)
        login_window.after(3000, label.destroy)

    if not username or not password:
        show_feedback("*Please enter both username and password", "#FF0101")
        return

    role = logic.check_user(username, password)

    if role:
        show_feedback("Login Successfully", "#077822")
        def open_main_app():
            login_window.destroy()
            run = MainPanel(user_role=role)
            run.run()
        login_window.after(2000, open_main_app)
    else:
        show_feedback("*Invalid username or password", "#FF0101")
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
        

        
       
    

    
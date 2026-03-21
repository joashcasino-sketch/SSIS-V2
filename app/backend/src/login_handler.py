import csv
import sys
import time
from pathlib import Path
from tkinter import messagebox, Label


BASE_DIR = Path(__file__).resolve().parent
frontend_src_path = BASE_DIR.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
sys.path.insert(0, str(frontend_src_path))

from main_panel import MainPanel

USER_CSV = BASE_DIR.parent / 'data' / 'users.csv'
class Login_Logic:

    def __init__(self, csv_path=USER_CSV):
        self.csv_path = csv_path
        self.setup_csv()

    def setup_csv(self):
        Path(self.csv_path).parent.mkdir(parents=True, exist_ok=True)

        if not Path(self.csv_path).exists():
            with open(self.csv_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['username', 'password', 'role'])
    def check_user(self, username, password):
        with open(self.csv_path, mode='r') as file:
            reader = csv.DictReader(file)

            for line in reader:
                if line['username'] == username and line['password'] == password:
                    return line.get('role', 'user')
            return None
    
    def register_user(self, username, password, role='user'):
        with open(self.csv_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([username, password, role])
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

    logic = Login_Logic()

    register = logic.register_user(username, password)

    if register:
        messagebox.showinfo("Success", "You are now Registered")
    else:
        messagebox.showerror("Error", "Invalid")
        

        
       
    

    
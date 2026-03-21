import tkinter as tk
from tkinter import messagebox, ttk

class UpdateCollegeDialog:
    def __init__(self, parent, controller, college_data):
        self.controller = controller
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit College")
        self.dialog.geometry("400x500")
        self.dialog.configure(bg="#F8ECD1")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        title = tk.Label(
            self.dialog,
            text="Edit College",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        )
        title.pack(fill="x")

        form = tk.Frame(self.dialog, padx=30, pady=20, bg="#F8ECD1")
        form.pack(padx=20, pady=10, fill="x")

        tk.Label(form, background="#F8ECD1", text="College Code:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.college_code_entry = tk.Entry(form, bg="#DEB6AB")
        self.college_code_entry.insert(0, college_data['College Code'])
        self.college_code_entry.config(state="disabled")  # ← dict key
        self.college_code_entry.grid(row=0, column=1, pady=10)

        tk.Label(form, background="#F8ECD1", text="College Name:", font=("Lato", 10)).grid(row=5, column=0, sticky="w", pady=5)
        self.college_name_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.college_name_entry.insert(0, college_data['College Name'])  # ← dict key
        self.college_name_entry.grid(row=5, column=1, pady=10)

        btn_frame = tk.Frame(self.dialog, bg="#F8ECD1",pady=20)
        btn_frame.pack()
        save_button = tk.Button(btn_frame,
                text="Save",
                font=("Lato", 10, "bold"),
                bg="#85586F", 
                fg="white",
                width=12,
                command=self.on_save,
                cursor="hand2"
        )
        save_button.pack(side="left", padx=10)

        cancel_button = tk.Button(btn_frame,
                text="Cancel",
                font=("Lato", 10, "bold"),
                bg="#D3D3D3", 
                fg="black",
                width=12,
                command=self.dialog.destroy,
                cursor="hand2"
        )
        cancel_button.pack(side="left", padx=10)
        
        self.dialog.transient(parent)
        self._center_window()

    def _center_window(self):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')

    def on_save(self):
        self.college_code_entry.config(state="normal")
        code = self.college_code_entry.get().strip()
        self.college_code_entry.config(state="disabled")

        college_data = {
            'College Code': code,
            'College Name': self.college_name_entry.get().strip()
        }

        if not all(college_data.values()):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        self.controller.update_college(college_data)
        self.dialog.destroy()
import csv
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / "backend" / "data"

def load_colleges():
    colleges = {}
    try:
        with open(DATA_PATH / "colleges.csv", newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                colleges[row["College Code"]] = row["College Name"]
    except FileNotFoundError:
        pass
    return colleges

def dropdown_style():
    return dict(
        bg="#DEB6AB",
        fg="black",
        relief="flat",
        borderwidth=2,
        highlightthickness=2,
        activebackground="#C9A090",
        cursor="hand2",
        indicatoron=False
    )

class UpdateProgramDialog:
    def __init__(self, parent, controller, program_data):
        self.controller = controller
        self.program_data = program_data
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Program")
        self.dialog.geometry("400x320")
        self.dialog.configure(bg="#F8ECD1")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        self.colleges = load_colleges()

        self.create_widgets()
        self.dialog.transient(parent)
        self._center_window()

    def _center_window(self):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')

    def create_widgets(self):
        tk.Label(
            self.dialog,
            text="Edit Program",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        ).pack(fill="x")

        form = tk.Frame(self.dialog, padx=30, pady=20, bg="#F8ECD1")
        form.pack(fill="both", expand=True)

        # Program Code (disabled)
        tk.Label(form, background="#F8ECD1", text="Program Code:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.program_code_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.program_code_entry.insert(0, self.program_data['Program Code'])
        self.program_code_entry.config(state="disabled")
        self.program_code_entry.grid(row=0, column=1, pady=10)

        # Program Name
        tk.Label(form, background="#F8ECD1", text="Program Name:", font=("Lato", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.program_name_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.program_name_entry.insert(0, self.program_data['Program Name'])
        self.program_name_entry.grid(row=1, column=1, pady=10)

        # College dropdown - pre-select current college
        tk.Label(form, background="#F8ECD1", text="College:", font=("Lato", 10)).grid(row=2, column=0, sticky="w", pady=10)
        college_options = [f"{code} - {name}" for code, name in self.colleges.items()]

        current_code = self.program_data['College Code']
        default_college = next(
            (opt for opt in college_options if opt.startswith(current_code + " - ")),
            college_options[0] if college_options else ""
        )

        self.college_var = tk.StringVar(value=default_college)
        college_menu = tk.OptionMenu(form, self.college_var, *college_options if college_options else ["No colleges"])
        college_menu.config(width=35, **dropdown_style())
        college_menu["menu"].config(
            bg="#DEB6AB", fg="black",
            activebackground="#85586F", activeforeground="white",
            borderwidth=0, relief="flat"
        )
        college_menu.grid(row=2, column=1, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#F8ECD1", pady=20)
        btn_frame.pack()

        tk.Button(btn_frame, text="Save", font=("Lato", 10, "bold"),
                  bg="#85586F", fg="white", width=12,
                  command=self.on_save, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Cancel", font=("Lato", 10, "bold"),
                  bg="#D3D3D3", fg="black", width=12,
                  command=self.dialog.destroy, cursor="hand2").pack(side="left", padx=10)

    def on_save(self):
        self.program_code_entry.config(state="normal")
        code = self.program_code_entry.get().strip()
        self.program_code_entry.config(state="disabled")

        college_raw = self.college_var.get()
        college_code = college_raw.split(" - ")[0]
        college_name = college_raw.split(" - ", 1)[1] if " - " in college_raw else ""

        program_data = {
            'Program Code': code,
            'Program Name': self.program_name_entry.get().strip(),
            'College Code': college_code,
            'College Name': college_name
        }

        if not all(program_data.values()):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        self.controller.update_program(program_data)
        self.dialog.destroy()
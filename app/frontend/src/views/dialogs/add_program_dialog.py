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

class AddProgramDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Program")
        self.dialog.geometry("400x350")
        self.dialog.configure(background="#F8ECD1")
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
            text="Add New Program",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        ).pack(fill="x")

        form = tk.Frame(self.dialog, padx=30, pady=20, bg="#F8ECD1")
        form.pack(fill="both", expand=True)

        # Program Code
        tk.Label(form, background="#F8ECD1", text="Program Code:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.code_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.code_entry.grid(row=0, column=1, pady=10)

        # Program Name
        tk.Label(form, background="#F8ECD1", text="Program Name:", font=("Lato", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.name_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.name_entry.grid(row=1, column=1, pady=10)

        # College dropdown
        tk.Label(form, background="#F8ECD1", text="College:", font=("Lato", 10)).grid(row=2, column=0, sticky="w", pady=10)
        college_options = [f"{code} - {name}" for code, name in self.colleges.items()]
        self.college_var = tk.StringVar(value=college_options[0] if college_options else "")
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
        college_raw = self.college_var.get()
        college_code = college_raw.split(" - ")[0]
        college_name = college_raw.split(" - ")[1] if " - " in college_raw else ""

        program_data = {
            'Program Code': self.code_entry.get().strip(),
            'Program Name': self.name_entry.get().strip(),
            'College Code': college_code,
            'College Name': college_name
        }

        if not program_data['Program Code'] or not program_data['Program Name']:
            messagebox.showerror("Error", "Program Code and Program Name are required!")
            return

        self.controller.add_program_from_dialog(program_data)
        self.dialog.destroy()
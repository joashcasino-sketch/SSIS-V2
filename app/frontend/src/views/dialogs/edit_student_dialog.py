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

def load_programs_by_college(college_code):
    programs = []
    try:
        with open(DATA_PATH / "programs.csv", newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if row["College Code"] == college_code:
                    programs.append(row["Program Code"])
    except FileNotFoundError:
        pass
    return programs

class UpdateStudentDialog:
    def __init__(self, parent, controller, student_data):
        self.controller = controller
        self.student_data = student_data
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Edit Student")
        self.dialog.geometry("400x500")
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

    def on_college_select(self, *args):
        selected_code = self.college_var.get().split(" - ")[0]
        programs = load_programs_by_college(selected_code)

        self.program_var.set("")
        self.program_menu["menu"].delete(0, "end")

        if programs:
            for prog in programs:
                self.program_menu["menu"].add_command(
                    label=prog,
                    command=lambda p=prog: self.program_var.set(p)
                )
            # Pre-select existing program if it's in the list, else default to first
            if self.student_data['Program'] in programs:
                self.program_var.set(self.student_data['Program'])
            else:
                self.program_var.set(programs[0])
        else:
            self.program_menu["menu"].add_command(label="No programs found", command=lambda: None)

    def dropdown_style(self):
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

    def create_widgets(self):
        tk.Label(
            self.dialog,
            text="Edit Student",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        ).pack(fill="x")

        form = tk.Frame(self.dialog, padx=30, pady=20, bg="#F8ECD1")
        form.pack(padx=20, pady=10, fill="x")

        # ID Number (disabled)
        tk.Label(form, background="#F8ECD1", text="ID Number:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.id_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.id_entry.insert(0, self.student_data['ID Number'])
        self.id_entry.config(state="disabled")
        self.id_entry.grid(row=0, column=1, pady=10)

        # Name
        tk.Label(form, background="#F8ECD1", text="Name:", font=("Lato", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(form, bg="#DEB6AB", font=("Lato", 10), width=30)
        self.name_entry.insert(0, self.student_data['Name'])
        self.name_entry.grid(row=1, column=1, pady=10)

        # Gender
        tk.Label(form, background="#F8ECD1", text="Gender:", font=("Lato", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.gender_var = tk.StringVar(value=self.student_data['Gender'])
        gender_frame = tk.Frame(form, bg="#F8ECD1")
        gender_frame.grid(row=2, column=1, sticky="w", pady=10)
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Male", variable=self.gender_var, value="Male").pack(side="left")
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Female", variable=self.gender_var, value="Female").pack(side="left")

        # Year Level
        tk.Label(form, background="#F8ECD1", text="Year Level:", font=("Lato", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.year_var = tk.StringVar(value=self.student_data['Year Level'])
        year_dropdown = tk.OptionMenu(form, self.year_var, "1", "2", "3", "4")
        year_dropdown.config(width=35, **self.dropdown_style())
        year_dropdown.grid(row=3, column=1, pady=10)

        # College dropdown - pre-select student's current college
        tk.Label(form, background="#F8ECD1", text="College:", font=("Lato", 10)).grid(row=4, column=0, sticky="w", pady=5)
        college_options = [f"{code} - {name}" for code, name in self.colleges.items()]

        # Find the matching option for the student's current college code
        current_college = self.student_data['College']
        default_college = next(
            (opt for opt in college_options if opt.startswith(current_college + " - ")),
            college_options[0] if college_options else ""
        )

        self.college_var = tk.StringVar(value=default_college)
        self.college_var.trace("w", self.on_college_select)
        college_menu = tk.OptionMenu(form, self.college_var, *college_options if college_options else ["No colleges"])
        college_menu.config(width=35, **self.dropdown_style())
        college_menu.grid(row=4, column=1, pady=10)

        # Program dropdown
        tk.Label(form, background="#F8ECD1", text="Program:", font=("Lato", 10)).grid(row=5, column=0, sticky="w", pady=5)
        self.program_var = tk.StringVar()
        self.program_menu = tk.OptionMenu(form, self.program_var, "")
        self.program_menu.config(width=35, **self.dropdown_style())
        self.program_menu.grid(row=5, column=1, pady=10)

        # Trigger initial load (will pre-select existing program)
        self.on_college_select()

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
        self.id_entry.config(state="normal")
        id_value = self.id_entry.get()
        self.id_entry.config(state="disabled")

        college_code = self.college_var.get().split(" - ")[0]

        student_data = {
            'ID Number': id_value,
            'Name': self.name_entry.get().strip(),
            'Gender': self.gender_var.get(),
            'Year Level': self.year_var.get(),
            'Program': self.program_var.get(),
            'College': college_code
        }

        if not all(student_data.values()):
            messagebox.showwarning("Incomplete", "Please fill in all fields.")
            return

        self.controller.update_student(student_data)
        self.dialog.destroy()
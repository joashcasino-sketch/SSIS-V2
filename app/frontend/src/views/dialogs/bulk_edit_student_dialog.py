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

def dropdown_style():
    return dict(
        bg="#DEB6AB", fg="black",
        relief="flat", borderwidth=2,
        highlightthickness=2,
        activebackground="#C9A090",
        cursor="hand2", indicatoron=False
    )

class BulkEditStudentDialog:
    def __init__(self, parent, controller, student_ids):
        self.controller = controller
        self.student_ids = student_ids  # list of ID Numbers

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Bulk Edit Students")
        self.dialog.geometry("420x380")
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
            self.program_var.set(programs[0])
        else:
            self.program_menu["menu"].add_command(label="No programs found", command=lambda: None)

    def create_widgets(self):
        tk.Label(
            self.dialog,
            text=f"Bulk Edit — {len(self.student_ids)} Student(s)",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        ).pack(fill="x")

        tk.Label(
            self.dialog,
            text="Leave a field unchanged to keep existing values.",
            font=("Lato", 9, "italic"),
            background="#F8ECD1",
            foreground="#642D48"
        ).pack(pady=(8, 0))

        form = tk.Frame(self.dialog, padx=30, pady=10, bg="#F8ECD1")
        form.pack(fill="both", expand=True)

        # Gender
        tk.Label(form, background="#F8ECD1", text="Gender:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.gender_var = tk.StringVar(value="— no change —")
        gender_frame = tk.Frame(form, bg="#F8ECD1")
        gender_frame.grid(row=0, column=1, sticky="w", pady=10)
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="No change", variable=self.gender_var, value="— no change —").pack(side="left")
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Male", variable=self.gender_var, value="Male").pack(side="left")
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Female", variable=self.gender_var, value="Female").pack(side="left")

        # Year Level
        tk.Label(form, background="#F8ECD1", text="Year Level:", font=("Lato", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.year_var = tk.StringVar(value="— no change —")
        year_menu = tk.OptionMenu(form, self.year_var, "— no change —", "1", "2", "3", "4")
        year_menu.config(width=35, **dropdown_style())
        year_menu["menu"].config(bg="#DEB6AB", fg="black", activebackground="#85586F", activeforeground="white", borderwidth=0, relief="flat")
        year_menu.grid(row=1, column=1, pady=10)

        # College
        tk.Label(form, background="#F8ECD1", text="College:", font=("Lato", 10)).grid(row=2, column=0, sticky="w", pady=10)
        college_options = ["— no change —"] + [f"{code} - {name}" for code, name in self.colleges.items()]
        self.college_var = tk.StringVar(value="— no change —")
        self.college_var.trace("w", self.on_college_select)
        college_menu = tk.OptionMenu(form, self.college_var, *college_options)
        college_menu.config(width=35, **dropdown_style())
        college_menu["menu"].config(bg="#DEB6AB", fg="black", activebackground="#85586F", activeforeground="white", borderwidth=0, relief="flat")
        college_menu.grid(row=2, column=1, pady=10)

        # Program
        tk.Label(form, background="#F8ECD1", text="Program:", font=("Lato", 10)).grid(row=3, column=0, sticky="w", pady=10)
        self.program_var = tk.StringVar(value="— no change —")
        self.program_menu = tk.OptionMenu(form, self.program_var, "— no change —")
        self.program_menu.config(width=35, **dropdown_style())
        self.program_menu["menu"].config(bg="#DEB6AB", fg="black", activebackground="#85586F", activeforeground="white", borderwidth=0, relief="flat")
        self.program_menu.grid(row=3, column=1, pady=10)

        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#F8ECD1", pady=15)
        btn_frame.pack()

        tk.Button(btn_frame, text="Save", font=("Lato", 10, "bold"),
                  bg="#85586F", fg="white", width=12,
                  command=self.on_save, cursor="hand2").pack(side="left", padx=10)

        tk.Button(btn_frame, text="Cancel", font=("Lato", 10, "bold"),
                  bg="#D3D3D3", fg="black", width=12,
                  command=self.dialog.destroy, cursor="hand2").pack(side="left", padx=10)

    def on_save(self):
        changes = {}

        if self.gender_var.get() != "— no change —":
            changes['Gender'] = self.gender_var.get()

        if self.year_var.get() != "— no change —":
            changes['Year Level'] = self.year_var.get()

        if self.college_var.get() != "— no change —":
            changes['College'] = self.college_var.get().split(" - ")[0]

        if self.program_var.get() != "— no change —":
            changes['Program'] = self.program_var.get()

        if not changes:
            messagebox.showwarning("No Changes", "No fields were changed.")
            return

        self.controller.bulk_edit_students(self.student_ids, changes)
        self.dialog.destroy()
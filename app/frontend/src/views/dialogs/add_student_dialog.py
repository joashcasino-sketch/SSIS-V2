import sys
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

CONTROLLER_PATH = Path(__file__).resolve().parent.parent.parent.parent.parent / 'backend' / 'src' / 'Controller'
sys.path.insert(0, str(CONTROLLER_PATH))
from college_controller import CollegeController
from program_controller import ProgramController

class AddStudentDialog:
    def __init__(self, parent, controller):
        self.controller = controller
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Student")
        self.dialog.geometry("400x500")
        self.dialog.configure(background="#F8ECD1")
        self.dialog.resizable(False, False)
        self.dialog.grab_set()

        college_ctrl = CollegeController(None, user_role="user")
        self.colleges = {
            row["College Code"]: row["College Name"]
            for row in college_ctrl.get_all_colleges()

        }

        self.create_widgets()
        self.dialog.transient(parent)
        self._center_window()

    def _center_window(self):
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (self.dialog.winfo_width() // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (self.dialog.winfo_height() // 2)
        self.dialog.geometry(f'+{x}+{y}')

    def _validate_id(self, new_value):
        if len(new_value) > 9:
            return False
        return all(c.isdigit() or c == '-' for c in new_value) or new_value == ""

    def on_college_select(self, *args):
        selected_code = self.college_var.get().split(" - ")[0]  
        prog_ctrl = ProgramController(None, user_role="user")
        programs = prog_ctrl.get_programs_by_college(selected_code)
        program_codes = [row["Program Code"] for row in programs]

        self.program_var.set("")
        self.program_menu["menu"].delete(0, "end")

        if program_codes:
            for prog in program_codes:
                self.program_menu["menu"].add_command(
                    label=prog,
                    command=lambda p=prog: self.program_var.set(p)
                )
            self.program_var.set(program_codes[0])
        else:
            self.program_menu["menu"].add_command(
                label="No programs found", command=lambda: None
            )

    def create_widgets(self):
        title = tk.Label(
            self.dialog,
            text="Add New Student",
            font=("Lato", 16, "bold"),
            background="#85586F",
            foreground="white",
            pady=15
        )
        title.pack(fill="x")

        form_frame = tk.Frame(self.dialog, padx=30, pady=20, bg="#F8ECD1")
        form_frame.pack(fill="both", expand=True)

        
        
        vcmd = (self.dialog.register(self._validate_id), "%P")
        tk.Label(form_frame, background="#F8ECD1", text="ID Number:", font=("Lato", 10)).grid(row=0, column=0, sticky="w", pady=10)
        self.id_entry = tk.Entry(form_frame, bg="#DEB6AB", font=("Lato", 10), width=10,
                validate="key", validatecommand=vcmd)
        self.id_entry.grid(row=0, column=1, pady=10)


        # First Name
        tk.Label(form_frame, background="#F8ECD1", text="First Name:", font=("Lato", 10)).grid(row=1, column=0, sticky="w", pady=10)
        self.first_name_entry = tk.Entry(form_frame, bg="#DEB6AB", font=("Lato", 10), width=25)
        self.first_name_entry.grid(row=1, column=1, pady=10)

        # Last Name
        tk.Label(form_frame, background="#F8ECD1", text="Last Name:", font=("Lato", 10)).grid(row=2, column=0, sticky="w", pady=10)
        self.last_name_entry = tk.Entry(form_frame, bg="#DEB6AB", font=("Lato", 10), width=25)
        self.last_name_entry.grid(row=2, column=1, pady=10)

        # Gender
        tk.Label(form_frame, background="#F8ECD1", text="Gender:", font=("Lato", 10)).grid(row=3, column=0, sticky="w", pady=10)
        self.gender_var = tk.StringVar(value="Male")
        gender_frame = tk.Frame(form_frame, bg="#F8ECD1")
        gender_frame.grid(row=3, column=1, sticky="w", pady=10)
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Male", variable=self.gender_var, value="Male").pack(side="left")
        tk.Radiobutton(gender_frame, bg="#F8ECD1", text="Female", variable=self.gender_var, value="Female").pack(side="left")

        # Year Level
        tk.Label(form_frame, background="#F8ECD1", text="Year Level:", font=("Lato", 10)).grid(row=4, column=0, sticky="w", pady=10)
        self.year_var = tk.StringVar(value="1")
        year_dropdown = tk.OptionMenu(form_frame, self.year_var, "1", "2", "3", "4")
        year_dropdown.config(
             width=35,
            bg="#DEB6AB",
            fg="black",
            relief="flat",          
            borderwidth=2,          
            highlightthickness=2,  
            activebackground="#C9A090",
            cursor="hand2",
            indicatoron=False
        )
        year_dropdown.grid(row=4, column=1, pady=10)

        # College dropdown
        tk.Label(form_frame, background="#F8ECD1", text="College:", font=("Lato", 10)).grid(row=5, column=0, sticky="w", pady=10)
        college_options = [f"{code} - {name}" for code, name in self.colleges.items()]
        self.college_var = tk.StringVar(value=college_options[0] if college_options else "")
        self.college_var.trace("w", self.on_college_select)
        college_menu = tk.OptionMenu(form_frame, self.college_var, *college_options if college_options else ["No colleges"])
        college_menu.config(
            width=35,
            bg="#DEB6AB",
            fg="black",
            relief="flat",          # ← removes the raised border
            borderwidth=2,          # ← removes border width
            highlightthickness=2,   # ← removes focus highlight ring
            activebackground="#C9A090",
            cursor="hand2",
            indicatoron=False       # ← removes the arrow indicator on the right
        )
        college_menu.grid(row=5, column=1, pady=10)

        # Program dropdown (populated after college is selected)
        tk.Label(form_frame, background="#F8ECD1", text="Program:", font=("Lato", 10)).grid(row=6, column=0, sticky="w", pady=10)
        self.program_var = tk.StringVar()
        self.program_menu = tk.OptionMenu(form_frame, self.program_var, "")
        self.program_menu.config(
            width=35,
            bg="#DEB6AB",
            fg="black",
            relief="flat",          
            borderwidth=2,          
            highlightthickness=2,  
            activebackground="#C9A090",
            cursor="hand2",
            indicatoron=False
        )
        self.program_menu.grid(row=6, column=1, pady=10)

        # Trigger initial program load
        self.on_college_select()

        # Buttons
        button_frame = tk.Frame(self.dialog, bg="#F8ECD1", pady=20)
        button_frame.pack()

        tk.Button(button_frame, text="Save", font=("Lato", 10, "bold"),
                  background="#85586F", foreground="white", width=12,
                  command=self.on_save, cursor="hand2").pack(side="left", padx=10)

        tk.Button(button_frame, text="Cancel", font=("Lato", 10, "bold"),
                  background="#D3D3D3", foreground="black", width=12,
                  command=self.dialog.destroy, cursor="hand2").pack(side="left", padx=10)

    def on_save(self):
        first_name = self.first_name_entry.get().strip()
        last_name  = self.last_name_entry.get().strip()
        student_id = self.id_entry.get().strip()

        if not student_id or not first_name or not last_name:
            messagebox.showerror("Error", "ID Number, First Name, and Last Name are required!")
            return

        student_data = {
            "ID Number":  student_id,
            "First Name": first_name,
            "Last Name":  last_name,
            "Gender":     self.gender_var.get(),
            "Year Level": self.year_var.get(),
            "Program":    self.program_var.get(),
        }

        self.controller.add_student_from_dialog(student_data)
        self.dialog.destroy()
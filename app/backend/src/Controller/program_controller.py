import sys
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
program_view_path = BASE_DIR.parent.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
program_model_path = BASE_DIR.parent / 'Model' 
sys.path.insert(0, str(program_view_path))
sys.path.insert(0, str(program_model_path))

from program_model import ProgramModel

class ProgramController:
    def __init__(self, views, user_role):
        self.model = ProgramModel()
        self.views = views
        self.user_role = user_role

    def add_program_from_dialog(self, program_data):
        success = self.model.add_program(program_data)

        if success:
            messagebox.showinfo("Success", "Program Added Successfully!")
            self.views.populate_programs()
        else:
            messagebox.showerror("Error", "Program ID Already Exist!")
        return success
    
    def update_program(self, program_data):
        success = self.model.edit_program(program_data)

        if success:
            messagebox.showinfo("Success", "Program has been updated!")
            self.views.populate_programs()
        else:
            messagebox.showerror("Error", "Please enter all required fields!")
        return success

    def delete_program(self, program_code):
        if self.model.program_has_students(program_code):
            messagebox.showwarning(
                "Cannot Delete",
                f"Program '{program_code}' currently has enrolled students\n"
                "Delete or reasign the students first."
            )
            return

        success = self.model.delete_program(program_code)
        if success:
            messagebox.showinfo("Success", "Program deleted successfully")
            self.views.populate_programs()
        else:
            messagebox.showerror("Error", "program not found.")

    def bulk_delete_programs(self, program_codes):
        blocked = []
        deleted = []

        for code in program_codes:
            if self.model.program_has_students(str(code)):
                blocked.append(str(code))
            else:
                success = self.model.delete_program(str(code))
                if success:
                    deleted.append(str(code))

        if deleted:
            messagebox.showinfo("Success", f"{len(deleted)} program(s) deleted.")

        if blocked:
            messagebox.showwarning(
                "Cannot Delete",
                f"The following program(s) still have enrolled students:\n"
                f"{', '.join(blocked)}\nDelete or reassign their students first."
            )

        self.views.populate_programs()

    def search_program(self, query):
        try:
            results = self.model.search_program(query)
            self.views.populate_programs(results)
        except Exception as e:
            print(f"Search error: {e}")

    def sort_program(self, column, reverse=False):
        try:
            results = self.model.sort_program(column, reverse)
            self.views.populate_programs(results)
        except Exception as e:
            print(f"Sort error: {e}")

    
        
import sys
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
college_view_path = BASE_DIR.parent.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
college_model_path = BASE_DIR.parent / 'Model' 
sys.path.insert(0, str(college_view_path))
sys.path.insert(0, str(college_model_path))

from college_model import CollegeModel

class CollegeController:
    def __init__(self, views, user_role):
        self.model = CollegeModel()
        self.views = views
        self.user_role = user_role

    def add_college_from_dialog(self, college_data):
        success = self.model.add_college(college_data)

        if success:
            messagebox.showinfo("Success", "Program Added Successfully!")
            self.views.populate_college()
        else:
            messagebox.showerror("Error", "Program ID Already Exist!")
        return success
    
    def update_college(self, college_data):
        success = self.model.edit_college(college_data)

        if success:
            messagebox.showinfo("Success", "Program has been updated!")
            self.views.populate_college()
        else:
            messagebox.showerror("Error", "Please enter all required fields!")
        return success

    def delete_college(self, college_code):
        if self.model.college_has_programs(college_code):
            messagebox.showwarning(
                "Cannot Delete",
                f"College '{college_code}' currently has programs\n"
                "Delete or reasign the students first."
            )
            return

        success = self.model.delete_college(college_code)
        if success:
            messagebox.showinfo("Success", "College deleted successfully")
            self.views.populate_college()
        else:
            messagebox.showerror("Error", "College not found.")

    def bulk_delete_colleges(self, college_codes):
        blocked = []
        deleted = []

        for code in college_codes:
            if self.model.college_has_programs(str(code)):
                blocked.append(str(code))
            else:
                success = self.model.delete_college(str(code))
                if success:
                    deleted.append(str(code))

        if deleted:
            messagebox.showinfo("Success", f"{len(deleted)} college(s) deleted.")

        if blocked:
            messagebox.showwarning(
                "Cannot Delete",
                f"The following college(s) still have programs:\n"
                f"{', '.join(blocked)}\nDelete or reassign their programs first."
            )

        self.views.populate_college()

    def search_college(self, query):
        try:
            results = self.model.search_college(query)
            self.views.populate_college(results)
        except Exception as e:
            print(f"Search error: {e}")

    def sort_college(self, column, reverse=False):
        try:
            results = self.model.sort_college(column, reverse)
            self.views.populate_college(results)
        except Exception as e:
            print(f"Sort error: {e}") 

    
        
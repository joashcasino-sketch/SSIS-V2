import sys
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent
student_view_path = BASE_DIR.parent.parent.parent / 'frontend' / 'src' / 'views' / 'panels'
student_model_path = BASE_DIR.parent / 'Model' 
sys.path.insert(0, str(student_view_path))
sys.path.insert(0, str(student_model_path))

from student_model import StudentModel

class StudentController:
    def __init__(self, views, user_role):
        self.model = StudentModel()
        self.views = views
        self.user_role = user_role

    def add_student_from_dialog(self, student_data):
        success = self.model.add_student(student_data)

        if success:
            messagebox.showinfo("Success", "Student Added Successfully!")
            self.views.populate_students()
        else:
            messagebox.showerror("Error", "Student ID Already Exist!")
        return success
    
    def update_student(self, student_data):
        success = self.model.edit_student(student_data)

        if success:
            messagebox.showinfo("Success", "Student has been updated!")
            self.views.populate_students()
        else:
            messagebox.showerror("Error", "Please enter all required fields!")
        return success

    def delete_student(self, student_id):
        success = self.model.delete_student(student_id)
        if success:
            messagebox.showinfo("Success", "Student deleted successfully")
            self.views.populate_students()
        else:
            messagebox.showerror("Error", "Student not found.")

    def bulk_delete_students(self, student_ids):
        for student_id in student_ids:
            self.model.delete_student(str(student_id))
        messagebox.showinfo("Success", f"{len(student_ids)} student(s) deleted.")
        self.views.populate_students()

    def search_student(self, query):
        try:
            results = self.model.search_student(query)
            self.views.populate_students(results)
        except Exception as e:
            print(f"Search error: {e}")

    def sort_student(self, column, reverse=False):
        try:
            results = self.model.sort_student(column, reverse)
            self.views.populate_students(results)
        except Exception as e:
            print(f"Sort error: {e}")
        
    def bulk_edit_students(self, student_ids, changes):
        success_count = 0
        for student_id in student_ids:
            if self.model.bulk_edit_student(str(student_id), changes):
                success_count += 1
        messagebox.showinfo("Success", f"{success_count} student(s) updated.")
        self.views.populate_students() 
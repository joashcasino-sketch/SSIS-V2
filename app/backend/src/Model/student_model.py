import csv
from os import read
from pathlib import Path

student_csv = Path(__file__).resolve().parent.parent.parent / 'data' / 'students.csv'
class StudentModel:
    def __init__(self):
        self.csv_file = student_csv
        self.headers = ['ID Number', 'Name', 'Gender', 'Year Level', 'Program', 'College']

    def add_student(self, student_data):
        try:
            if self.student_exist(student_data.get('ID Number')):
                return False
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(student_data)

                return True
            
        except Exception as e:
            print(f"Error adding students: {e}")
            return False
        
    def student_exist(self, student_id):
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID Number'] == student_id:
                        return True
            return False
        except FileNotFoundError:
            return False
        
    def edit_student(self, student_data):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["ID Number"] == student_data.get("ID Number"):
                        rows.append(student_data)
                        found = True
                    else:
                        rows.append(row)

            if not found:
                return False
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)

            return True

        except Exception as e:
            print(f"Error update student: {e}")
            return False

    def delete_student(self, student_id):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['ID Number'] == student_id:
                        found = True
                    else:
                        rows.append(row)
            
            if not found:
                return False

            with open(self.csv_file, 'w', newline='', encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)

            return True
    
        except Exception as e:
            print(f"Error deleting student {e}")
            return False
    
    def search_student(self, query):
        try:
            results = []
            query = query.lower().strip()

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if any(query in str(value).lower() for value in row.values()):
                        results.append(row)

            return results
        
        except FileNotFoundError:
            return []
        
        except Exception as e:
            print(f"Search student error: {e}")
            return []
        
    def sort_student(self, column, reverse=False):
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            rows.sort(key=lambda row: row[column].lower(), reverse=reverse)
            return rows
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Sort student error: {e}")
            return []
        
    def bulk_edit_student(self, student_id, changes):
        try:
            rows = []
            found = False
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['ID Number'] == student_id:
                        row.update(changes)  
                        found = True
                    rows.append(row)

            if not found:
                return False

            with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=self.headers)
                writer.writeheader()
                writer.writerows(rows)

            return True
        except Exception as e:
            print(f"Bulk edit error: {e}")
            return False
import csv
from os import read
from pathlib import Path

program_csv = Path(__file__).resolve().parent.parent.parent / 'data' / 'programs.csv'
class ProgramModel:
    def __init__(self):
        self.csv_file = program_csv
        self.headers = ['Program Code', 'Program Name', 'College Code', 'College Name']

    def add_program(self, program_data):
        try:
            if self.program_exist(program_data.get('Program Code')):
                return False
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(program_data)

                return True
            
        except Exception as e:
            print(f"Error adding programs: {e}")
            return False
        
    def program_exist(self, program_code):
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Program Code'] == program_code:
                        return True
            return False
        except FileNotFoundError:
            return False
        
    def edit_program(self, program_data):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Program Code"] == program_data.get("Program Code"):
                        rows.append(program_data)
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
            print(f"Error update program: {e}")
            return False

    def delete_program(self, program_id):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Program Code'] == program_id:
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
            print(f"Error deleting program {e}")
            return False
    
    def program_has_students(self, program_code):
        try:
            student_csv = self.csv_file.parent / 'students.csv'
            with open(student_csv, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["Program"] == program_code.strip():
                        return True    
            return False
        except FileNotFoundError:
            return False
        
    def sort_program(self, column, reverse=False):
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            rows.sort(key=lambda r: r.get(column, '').lower(), reverse=reverse)
            return rows

        except Exception as e:
            print(f"Error sorting programs: {e}")
            return []
    
    def search_program(self, query):
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
            print(f"Search program error: {e}")
            return []
import csv
from pathlib import Path

college_csv = Path(__file__).resolve().parent.parent.parent / 'data' / 'colleges.csv'
class CollegeModel:
    def __init__(self):
        self.csv_file = college_csv
        self.headers = ['College Code', 'College Name']

    def add_college(self, college_data):
        try:
            if self.college_exist(college_data.get('College Code')):
                return False
            
            with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.headers)
                writer.writerow(college_data)

                return True
            
        except Exception as e:
            print(f"Error adding programs: {e}")
            return False
        
    def college_exist(self, college_code):
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['College Code'] == college_code:
                        return True
            return False
        except FileNotFoundError:
            return False
        
    def edit_college(self, college_data):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["College Code"] == college_data.get("College Code"):
                        rows.append(college_data)
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
            print(f"Error update college: {e}")
            return False

    def delete_college(self, college_code):
        try:
            rows = []
            found = False

            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['College Code'] == college_code:
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
            print(f"Error deleting college {e}")
            return False
        
    def search_college(self, query):
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
            print(f"Search college error: {e}")
            return []
    
    def college_has_programs(self, college_code):
        try:
            program_csv = self.csv_file.parent / 'programs.csv'
            with open(program_csv, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["College Code"] == college_code.strip():
                        return True    
            return False
        except FileNotFoundError:
            return False
        
    def sort_college(self, column, reverse=False):
        try:
            with open(self.csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                rows = list(reader)

            rows.sort(key=lambda r: r.get(column, '').lower(), reverse=reverse)
            return rows

        except Exception as e:
            print(f"Error sorting college: {e}")
            return []
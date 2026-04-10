import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" 
sys.path.insert(0, str(DB_PATH))

from db_connection import get_connection
from mysql.connector import Error
class StudentModel:
   
    def add_student(self, student_data):
        try:
            if self.student_exist(student_data.get('ID Number')):
                return False
            
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(""" 
                INSERT INTO students (student_id, student_first_name,
                           student_last_name, gender, student_year_level, program_code)
                VALUES(%s, %s, %s, %s, %s, %s)
            """, (
                student_data["ID Number"],
                student_data["First Name"],
                student_data["Last Name"],
                student_data["Gender"],
                student_data["Year Level"],
                student_data["Program"],
            ))
            conn.commit()
            return True
            
        except Exception as e:
            print(f"Error adding students: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
        
    def get_all_students(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT s.student_id          AS 'ID Number',
                   s.student_first_name  AS 'First Name',
                   s.student_last_name   AS 'Last Name',
                   s.gender              AS 'Gender',
                   s.student_year_level  AS 'Year Level',
                   s.program_code        AS 'Program',
                   c.college_code        AS 'College'
                FROM students s
                LEFT JOIN programs p ON s.program_code = p.program_code
                LEFT JOIN colleges c ON p.college_code = c.college_code
            """)
            return cursor.fetchall()

        except Error as e:
            print(f"Error fetching students: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def student_exist(self, student_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM students WHERE student_id = %s", (student_id,)
            )
            return cursor.fetchone() is not None
        except Error as e:
            print(f"Error checking students: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
        
    def edit_student(self, student_data):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE students
                SET student_first_name = %s,
                    student_last_name   = %s,
                    gender              = %s,
                    student_year_level  = %s,
                    program_code        = %s     
                WHERE student_id = %s     
            """, (
                student_data["First Name"],
                student_data["Last Name"],
                student_data["Gender"],
                student_data["Year Level"],
                student_data["Program"],
                student_data["ID Number"],
            ))
            conn.commit()
            return cursor.rowcount > 0

        except Error as e:
            print(f"Error editing student: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_student(self, student_id):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            conn.commit()
            return cursor.rowcount > 0
        
        except Error as e:
            print(f"Error deleting student {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def search_student(self, query):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query.strip()}%"

            cursor.execute("""
                SELECT s.student_id         AS 'ID Number',
                    s.student_first_name AS 'First Name',
                    s.student_last_name  AS 'Last Name',
                    s.gender             AS 'Gender',
                    s.student_year_level AS 'Year Level',
                    s.program_code       AS 'Program',
                    c.college_code       AS 'College'
                FROM students s
                LEFT JOIN programs p ON s.program_code = p.program_code
                LEFT JOIN colleges c ON p.college_code = c.college_code
                WHERE s.student_id          LIKE %s
                OR    s.student_first_name  LIKE %s
                OR    s.student_last_name   LIKE %s
                OR    s.gender              LIKE %s
                OR    s.student_year_level  LIKE %s
                OR    s.program_code        LIKE %s
            """, (like,) * 6)
            return cursor.fetchall()
        
        except Error as e:
            print(f"Search student error: {e}")
            return []
        finally:
            cursor.close()
            conn.close(  )
        
    ALLOWED_COLUMNS = {
        "ID Number":   "s.student_id",
        "Name":        "s.student_last_name",
        "First Name":  "s.student_first_name",
        "Last Name":   "s.student_last_name",
        "Gender":      "s.gender",
        "Year Level":  "s.student_year_level",
        "Program":     "s.program_code",
        "College":     "c.college_code",
    }

    def sort_student(self, column, reverse=False):
        sql_col = self.ALLOWED_COLUMNS.get(column)
        if not sql_col:
            print(f"Invalid sort column: {column}")
            return []
        try:
            direction = "DESC" if reverse else "ASC"
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT s.student_id          AS 'ID Number',
                       s.student_first_name  AS 'First Name',
                       s.student_last_name   AS 'Last Name',
                       s.gender              AS 'Gender',
                       s.student_year_level  AS 'Year Level',
                       s.program_code        AS 'Program',
                       c.college_code        AS 'College'                           
                FROM students s
                LEFT JOIN programs p ON s.program_code = p.program_code
                LEFT JOIN colleges c ON p.college_code = c.college_code
                ORDER BY {sql_col} {direction}
            """)
            return cursor.fetchall()
        except Error as e:
            print(f"Sort student error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
        
    def bulk_edit_student(self, student_id, changes):
        allowed_fields = {
            "First Name":  "student_first_name",
            "Last Name":   "student_last_name",
            "Gender":      "gender",
            "Year Level":  "student_year_level",
            "Program":     "program_code",
        }
        fields = {allowed_fields[k]: v
                  for k, v in changes.items() if k in allowed_fields}
        if not fields:
            return False
        try:
            set_clause = ", ".join(f"{col} = %s" for col in fields)
            values = list(fields.values()) + [student_id]
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE students SET {set_clause} WHERE student_id = %s",
                values
            )
            conn.commit()
            return cursor.rowcount > 0

        except Error as e:
            print(f"Bulk edit error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
from pathlib import Path
from sqlite3 import Cursor
import sys

DB_PATH = Path(__file__).resolve().parent.parent / "db" 
sys.path.insert(0, str(DB_PATH))

from db_connection import get_connection
from mysql.connector import Error
   
class CollegeModel:

    def add_college(self, college_data):
        try:
            if self.program_exist(college_data.get('Program Code')):
                return False
                    
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(""" 
                    INSERT INTO colleges (college_code, college_name)
                    VALUES(%s, %s)
                """, (
                    college_data["College Code"],
                    college_data["College Name"],
                ))
            conn.commit()
            return True
                    
        except Exception as e:
                print(f"Error adding colleges: {e}")
                return False
        finally:
            cursor.close()
            conn.close()

    def get_all_colleges(self):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT college_code AS 'College Code',
                       college_name AS 'College Name'
                FROM colleges
            """)
            return cursor.fetchall()
 
        except Error as e:
            print(f"Error fetching colleges: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
        
    def college_exist(self, college_code):
        try:
           conn = get_connection()
           cursor = conn.cursor()
           cursor.execute("SELECT 1 FROM colleges WHERE college_code = %s", (college_code,))

           return cursor.fetchone() is not None
        except Error as e:
            print(f"Error checking college {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    def edit_college(self, college_data):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE colleges
                SET college_name = %s
                WHERE college_code = %s
            """, (
                college_data["College Name"],
                college_data["College Code"],
            ))
            conn.commit()
            return cursor.rowcount > 0
 
        except Error as e:
            print(f"Error editing college: {e}")
            return False
        finally:
            cursor.close()
            conn.close()


    def delete_college(self, college_code):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM colleges WHERE college_code = %s", (college_code,)
            )
            conn.commit()
            return cursor.rowcount > 0
 
        except Error as e:
            print(f"Error deleting college: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    def search_college(self, query):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query.strip()}%"
            cursor.execute("""
                SELECT college_code AS 'College Code',
                       college_name AS 'College Name'
                FROM colleges
                WHERE college_code LIKE %s
                OR college_name LIKE %s
            """, (like, like))
            return cursor.fetchall()
 
        except Error as e:
            print(f"Search college error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    def college_has_programs(self, college_code):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM programs WHERE college_code = %s LIMIT 1", (college_code,)
            )
            return cursor.fetchone() is not None
 
        except Error as e:
            print(f"Error checking college programs: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    ALLOWED_COLUMNS = {
        "College Code": "college_code",
        "College Name": "college_name",
    }
        
    def sort_college(self, column, reverse=False):
        sql_col = self.ALLOWED_COLUMNS.get(column)
        if not sql_col:
            print(f"Invalid sort column: {column}")
            return []
        try:
            direction = "DESC" if reverse else "ASC"
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT college_code AS 'College Code',
                       college_name AS 'College Name'
                FROM colleges
                ORDER BY {sql_col} {direction}
            """)
            return cursor.fetchall()
 
        except Error as e:
            print(f"Sort college error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
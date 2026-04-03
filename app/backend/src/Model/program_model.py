import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "db" 
sys.path.insert(0, str(DB_PATH))

from db_connection import get_connection
from mysql.connector import Error
class ProgramModel:

    def add_program(self, program_data):
        try:
            if self.program_exist(program_data.get('Program Code')):
                    return False
                
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute(""" 
                    INSERT INTO programs (program_code, program_name, college_code)
                    VALUES(%s, %s, %s)
                """, (
                    program_data["Program Code"],
                    program_data["Program Name"],
                    program_data["College Code"],
                ))
            conn.commit()
            return True
                
        except Exception as e:
                print(f"Error adding programs: {e}")
                return False
        finally:
                cursor.close()
                conn.close()

    def get_all_programs(self):
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT program_code AS 'Program Code',
                        program_name AS 'Program Name',
                        college_code AS 'College Code'
                    FROM programs
                """)
                return cursor.fetchall()
            except Error as e:
                print(f"Error fetching programs: {e}")
                return []
            finally:
                cursor.close()
                conn.close()

    def get_programs_by_college(self, college_code):
            try:
                conn = get_connection()
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT  program_code    AS 'Program Code',
                            program_name    AS 'Program Name',
                            college_code    AS 'College Code'
                    FROM programs
                    WHERE college_code = %s
                """, (college_code,))
                return cursor.fetchall()

            except Error as e:
                print(f"Error fetching programs by college: {e}")
                return []
            finally:
                cursor.close()
                conn.close()
            
    def program_exist(self, program_code):
            try:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT 1 FROM programs WHERE program_code = %s", (program_code,)
                )
                return cursor.fetchone() is not None
            except Error as e:
                print(f"Error checking programs: {e}")
                return False
            finally:
                cursor.close()
                conn.close()
            
    def edit_program(self, program_data):
            try:
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE programs
                    SET program_name    = %s,
                        college_code    = %s
                    WHERE program_code = %s     
                """, (
                    program_data["Program Name"],
                    program_data["College Code"],
                    program_data["Program Code"],
                ))
                conn.commit()
                return cursor.rowcount > 0

            except Error as e:
                print(f"Error editing programs: {e}")
                return False
            finally:
                cursor.close()
                conn.close()

    def delete_program(self, program_code):
        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM programs WHERE program_code = %s", (program_code,))
            conn.commit()
            return cursor.rowcount > 0
        
        except Error as e:
            print(f"Error deleting program {e}")
            return False
        finally:
            cursor.close()
            conn.close()
        
    def program_has_students(self, program_code):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM students WHERE program_code = %s LIMIT 1", (program_code,)
            )
            return cursor.fetchone() is not None

        except Error as e:
            print(f"Error checking program students: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

        
    ALLOWED_COLUMNS = {
        "Program Code": "program_code",
        "Program Name": "program_name",
        "College Code": "college_code",
    }

    def sort_program(self, column, reverse=False):
        sql_col = self.ALLOWED_COLUMNS.get(column)
        if not sql_col:
            print(f"Invalid sort column: {column}")
            return []
        try:
            direction = "DESC" if reverse else "ASC"
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(f"""
                SELECT program_code AS 'Program Code',
                    program_name AS 'Program Name',
                    college_code AS 'College Code'
                FROM programs
                ORDER BY {sql_col} {direction}
            """)
            return cursor.fetchall()

        except Error as e:
            print(f"Sort program error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    
    def search_program(self, query):
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            like = f"%{query.strip()}%"
            cursor.execute("""
                SELECT program_code AS 'Program Code',
                    program_name AS 'Program Name',
                    college_code AS 'College Code'
                FROM programs
                WHERE program_code LIKE %s
                OR program_name LIKE %s
                OR college_code LIKE %s
            """, (like,) * 3)
            return cursor.fetchall()

        except Error as e:
            print(f"Search program error: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="239204",
        database="ssis"
    )

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    conn.close()
except Exception as e:
    print("Connection failed:", e)
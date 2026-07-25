from modules.database import get_connection
conn = get_connection()
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(alerts)")
for row in cursor.fetchall():
    print(row)
conn.close()
from connection import get_connection


try:
    connection = get_connection()
    print("Successfully connected to Supabase PostgreSQL!")

    cursor = connection.cursor()
    cursor.execute("SELECT version();")

    version = cursor.fetchone()
    print("PostgreSQL version:")
    print(version[0])

    cursor.close()
    connection.close()

except Exception as error:
    print("Connection failed:")
    print(error)
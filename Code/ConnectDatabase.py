import mysql.connector

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="5749",
            database="math"
        )
        print("Database connected successfully!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

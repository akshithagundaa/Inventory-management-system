import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="inventory_db",
        user="postgres",
        password="postgres",
        host="localhost",
        port="5432"
    )
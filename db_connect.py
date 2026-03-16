import psycopg2


def get_connection():
    conn = psycopg2.connect(dbname="school", host="localhost", user="postgres", password="tolstik.1", port="5432")
    return conn

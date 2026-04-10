import psycopg
from pathlib import Path
from app.tools.config import get_db_host, get_db_name, get_db_user, get_db_password

HOST = "localhost"
NAME = "postgres"
USER = "postgres"
PASSWORD = "1234"

BASE_DIR = Path(__file__).resolve().parent
#hey guys welcome to my minecraft letsplay
#check existance of database
def read_sql_file(filename):
    file_path = BASE_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
#user нельзя, ключ слово
def create_db():
    try:
        sql = read_sql_file('../sql_scripts/create_database.sql')
        conn = psycopg.connect(host=HOST,
                               dbname=NAME,
                               user=USER,
                               password=PASSWORD,
                               autocommit=True)
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg.errors.DuplicateDatabase:
        print("Database already exists")



def createTables():
    sql = read_sql_file("../sql_scripts/create_all_tables.sql")
    conn = psycopg.connect(host=HOST,
                               dbname=NAME,
                               user=USER,
                               password=PASSWORD,
                               autocommit=True)
    cur = conn.cursor()

    cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()



def add_user(login, nickname, password_hash, about):

    conn = psycopg.connect(host=HOST,
                           dbname=NAME,
                           user=USER,
                           password=PASSWORD,
                           autocommit=True)
    cur = conn.cursor()

    cur.execute("""INSERT INTO users (login, nickname, password_hash, about)
        VALUES (%s, %s, %s, %s);
        """, (login, nickname, password_hash, about))

    conn.commit()
    cur.close()
    conn.close()
import psycopg
from pathlib import Path
from app.tools.config import get_db_host, get_db_name, get_db_user, get_db_password

HOST = get_db_host()
NAME = get_db_name()
USER = get_db_user()
PASSWORD = get_db_password()

BASE_DIR = Path(__file__).resolve().parent
#hey guys welcome to my minecraft letsplay
#check existance of database
def read_sql_file(filename):
    file_path = BASE_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
#user нельзя, ключ слово
def create_db():
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


import psycopg
from psycopg import sql
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

conn = psycopg.connect(host=HOST,
                               dbname=NAME,
                               user=USER,
                               password=PASSWORD,
                               autocommit=True)
cur = conn.cursor()



def create_db():
    try:
        sql = read_sql_file('../sql_scripts/create_database.sql')

        cur.execute(sql)
        conn.commit()

    except psycopg.errors.DuplicateDatabase:
        print("Database already exists")



def createTables():
    sql = read_sql_file("../sql_scripts/create_all_tables.sql")

    cur.execute(sql)
    conn.commit()




def add_user(login, nickname, password_hash, about):

    cur.execute("""INSERT INTO users (login, nickname, password_hash, about)
        VALUES (%s, %s, %s, %s);
        """, (login, nickname, password_hash, about))
    return get_user_attribute_by_login(login, "id")

    conn.commit()
def get_user_attribute_by_login(login, attribute):
    attribute = str(attribute)
    query = sql.SQL("""SELECT {row} FROM users WHERE login = %s;""").format(
        row=sql.Identifier(attribute))
    cur.execute(query, (login,))
    user_id = cur.fetchone()
    if user_id is None:
        return None
    else:
        return user_id[0]

#user exists func from previous
def user_exists(login):
    if get_user_attribute_by_login(login, "id") is None:
        return False
    else:
        return True

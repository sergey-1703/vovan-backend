import psycopg
from psycopg import sql
from pathlib import Path
from app.tools.config import get_db_host, get_db_name, get_db_user, get_db_password
HOST = get_db_host()
NAME = get_db_name()
USER = get_db_user()
PASSWORD = get_db_password()
conn: psycopg.connection
cur: psycopg.cursor
#for pl:
#"localhost"
#"postgres"
#"postgres"
#1234


def switch_to_test_env():
    global HOST, NAME, USER, PASSWORD
    HOST = "localhost"
    NAME = "postgres"
    USER = "postgres"
    PASSWORD = 1234
    connect()

BASE_DIR = Path(__file__).resolve().parent
#hey guys welcome to my minecraft letsplay
#check existance of database
def read_sql_file(filename):
    file_path = BASE_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
#user нельзя, ключ слово

def connect():
    global conn, cur
    try:
        conn = psycopg.connect(host=HOST,
                                   dbname=NAME,
                                   user=USER,
                                   password=PASSWORD,
                                   autocommit=True)
        cur = conn.cursor()
    except Exception as error:
        print("noooo")

connect()

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


def user_exists(login):
    if get_user_attribute_by_login(login, "id") is None:
        return False
    else:
        return True

def get_user_attribute_list_by_login(login,  size, offset = 0):
    #add for nickname or login
    login = f"%{login}%"
    query = sql.SQL("""SELECT id, login, nickname  FROM users WHERE login LIKE %s""")
    cur.execute(query, (login,))
    if offset!=0:
        cur.fetchmany(offset)
    user_id = cur.fetchmany(size)
    user_id_2 =[]
    for i in user_id:
        user_id_2.append(i)
    return user_id_2
#def change attribute by id (for about for example)
def change_attribute_by_id(id, attribute, new_attribute):
    attribute = str(attribute)
    query = sql.SQL("""UPDATE users SET {attribute} = %s WHERE id = %s;""").format(
        attribute=sql.Identifier(attribute),
    )
    cur.execute(query, (new_attribute, id))

    conn.commit()

def is_users_empty():
    cur.execute("""SELECT 1 FROM users LIMIT 1;""")
    rows_count = cur.rowcount
    return rows_count == 0

def add_test_users():
    if is_users_empty():
        sql = read_sql_file('../sql_scripts/generate_test_users.sql')

        cur.execute(sql)
        conn.commit()
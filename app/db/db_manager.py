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

def get_users_by_query(login,  size, id, offset = 0):
    #change to full sql
    login = f"%{login}%"
    query = sql.SQL("""SELECT id, login, nickname  FROM users 
                       WHERE (login LIKE %s OR nickname LIKE %s) AND id != %s
                       LIMIT %s OFFSET %s;
                    """)
    cur.execute(query, (login, login, id, size, offset))

    user_id = cur.fetchall()


    return user_id


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

def get_user_by_id(id):
    query = sql.SQL("""SELECT * FROM users WHERE id = %s;""")
    cur.execute(query, (id,))
    return cur.fetchone()




def chat_is_exists(chat_id):
    query = sql.SQL("""SELECT 1 FROM chats WHERE id = %s;""")
    cur.execute(query, (chat_id,))
    if cur.rowcount == 0:
        return False
    else:
        return True

def create_chat(user_main_id, user_chatter_id):
    cur.execute("""INSERT INTO chats (user_main_id, user_chatter_id)   VALUES (%s, %s) 
                RETURNING id;""",
                (user_main_id, user_chatter_id))
    return cur.fetchone()[0]

def track_message(user_main_id, chat_id, message):
    cur.execute("""INSERT INTO messages (user_main_id, chat_id, body) VALUES (%s, %s, %s) 
                RETURNING id;""",
                (user_main_id, chat_id, message))
    return cur.fetchone()[0]

def track_message_and_create_chat(sender, reciever, msg_body):
    chat_id = (create_chat(sender, reciever))
    track_message(sender, chat_id, msg_body)
    return chat_id

def get_user_chats(user_id, limit, offset = 0):
    query = sql.SQL("""SELECT id, user_chatter_id FROM chats WHERE user_main_id = %s
                    LIMIT %s OFFSET %s;""")
    cur.execute(query, (user_id, limit, offset))
    list_of_chats = cur.fetchall()
    final_list_of_chats = []
    for i in list_of_chats:
        chat_id = i[0]
        user_chatter_id = i[1]
        user_reciever_nickname = get_user_by_id(user_chatter_id)[2]
        last_message = get_last_message(user_id, chat_id)
        final_list_of_chats.append([chat_id, user_reciever_nickname, last_message])
    return final_list_of_chats

def get_messages(user_id, chat_id, limit, offset = 0):
    cur.execute("""SELECT user_main_id,body FROM messages WHERE user_main_id = %s AND chat_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;""",
                (user_id, chat_id, limit, offset))
    return cur.fetchall()

def get_last_message(user_id, chat_id):
    last_message = get_messages(user_id, chat_id, 1)
    if last_message == []:
        return None
    else: return last_message[0][1]

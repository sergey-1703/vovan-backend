import psycopg
from psycopg import sql
from pathlib import Path
from app.tools.config import get_db_host, get_db_name, get_db_user, get_db_password

HOST = get_db_host()
NAME = get_db_name()
USER = get_db_user()
PASSWORD = get_db_password()


def connect():
    global conn, cur
    conn = psycopg.connect(host=HOST,
                           dbname=NAME,
                           user=USER,
                           password=PASSWORD,
                           autocommit=True)
    cur = conn.cursor()


# for pl:
# "localhost"
# "postgres"
# "postgres"
# 1234


def switch_to_test_env():
    global HOST, NAME, USER, PASSWORD
    HOST = "localhost"
    NAME = "messenger_db"
    USER = "postgres"
    PASSWORD = 1234
    print("Switching to test environment")


BASE_DIR = Path(__file__).resolve().parent


# hey guys welcome to my minecraft letsplay
# check existance of database
def read_sql_file(filename):
    file_path = BASE_DIR / filename
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# user нельзя, ключ слово


def create_db():
    conn = psycopg.connect(host="localhost",
                           dbname="postgres",
                           user="postgres",
                           password=1234,
                           autocommit=True)
    cur = conn.cursor()
    try:
        sql = read_sql_file('../sql_scripts/create_database.sql')

        cur.execute(sql)
        conn.commit()


    except psycopg.errors.DuplicateDatabase:
        print("Database already exists")
    sql = read_sql_file('../sql_scripts/timezone_set_db.sql')

    cur.execute(sql)
    conn.commit()
    conn.close()


# switch_to_test_env()
create_db()
connect()


def createTables():
    global conn, cur
    sql = read_sql_file("../sql_scripts/create_all_tables.sql")

    cur.execute(sql)
    conn.commit()


def add_user(login, nickname, password_hash, about):
    global conn, cur
    cur.execute("""INSERT INTO users (login, nickname, password_hash, about)
        VALUES (%s, %s, %s, %s);
        """, (login, nickname, password_hash, about))
    return get_user_attribute_by_login(login, "id")


def get_user_attribute_by_login(login, attribute):
    global conn, cur
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
    global conn, cur
    if get_user_attribute_by_login(login, "id") is None:
        return False
    else:
        return True


def get_users_by_query(login, size, id, offset=0):
    global conn, cur
    login = f"%{login}%"
    query = sql.SQL("""SELECT id, login, nickname  FROM users 
                       WHERE (login LIKE %s OR nickname LIKE %s) AND id != %s
                       LIMIT %s OFFSET %s;
                    """)
    cur.execute(query, (login, login, id, size, offset))

    user_id = cur.fetchall()

    return user_id


def change_attribute_by_id(id, attribute, new_attribute):
    global conn, cur
    attribute = str(attribute)
    query = sql.SQL("""UPDATE users SET {attribute} = %s WHERE id = %s;""").format(
        attribute=sql.Identifier(attribute),
    )
    cur.execute(query, (new_attribute, id))

    conn.commit()


def is_users_empty():
    global conn, cur
    cur.execute("""SELECT 1 FROM users LIMIT 1;""")
    rows_count = cur.rowcount
    return rows_count == 0


def is_messages_empty():
    global conn, cur
    cur.execute("""SELECT 1 FROM messages LIMIT 1;""")
    rows_count = cur.rowcount
    return rows_count == 0


def add_test_data():
    global conn, cur
    if is_users_empty():
        sql = read_sql_file('../sql_scripts/generate_test_users.sql')
        cur.execute(sql)
        conn.commit()
    if is_messages_empty():
        sql = read_sql_file('../sql_scripts/generated_chats_messages.sql')
        cur.execute(sql)
        conn.commit()


def get_user_by_id(id):
    global conn, cur
    query = sql.SQL("""SELECT * FROM users WHERE id = %s;""")
    cur.execute(query, (id,))
    return cur.fetchone()


def chat_is_exists(chat_id):
    global conn, cur
    query = sql.SQL("""SELECT 1 FROM chats WHERE id = %s;""")
    cur.execute(query, (chat_id,))
    if cur.rowcount == 0:
        return False
    else:
        return True


def create_chat(user_main_id, user_chatter_id):
    global conn, cur
    reset_chat_id_sequence()
    cur.execute("""INSERT INTO chats (user_main_id, user_chatter_id)   VALUES (%s, %s) 
                RETURNING id;""",
                (user_main_id, user_chatter_id))
    return cur.fetchone()[0]


def track_message(user_main_id, chat_id, message):
    global conn, cur
    reset_messages_id_sequence()
    cur.execute("""INSERT INTO messages (user_main_id, chat_id, body) VALUES (%s, %s, %s) 
                RETURNING id;""",
                (user_main_id, chat_id, message))
    return cur.fetchone()[0]


def track_message_and_create_chat(sender, reciever, msg_body):
    chat_id = (create_chat(sender, reciever))
    track_message(sender, chat_id, msg_body)
    return chat_id


def get_user_chats(user_id, limit, offset=0):
    global conn, cur
    query = sql.SQL("""SELECT id, 
                    CASE
            WHEN user_main_id = %s THEN user_chatter_id
            WHEN user_chatter_id = %s THEN user_main_id
        END AS receiver_id FROM chats WHERE user_main_id = %s OR user_chatter_id = %s
                    LIMIT %s OFFSET %s;""")
    cur.execute(query, (user_id, user_id, user_id, user_id, limit, offset))
    list_of_chats = cur.fetchall()
    final_list_of_chats = []
    for i in list_of_chats:
        chat_id = i[0]
        user_receiver_id = i[1]
        user_receiver_nickname = get_user_by_id(user_receiver_id)[2]
        last_message = get_last_message(user_id, chat_id)
        final_list_of_chats.append([chat_id, user_receiver_id, user_receiver_nickname, last_message])
    return final_list_of_chats


def get_messages_from_user_from_chat(user_id, chat_id, limit, offset=0):
    global conn, cur
    cur.execute("""SELECT user_main_id,body FROM messages WHERE user_main_id = %s AND chat_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;""",
                (user_id, chat_id, limit, offset))
    return cur.fetchall()


def get_last_message(user_id, chat_id):
    global conn, cur
    last_message = get_messages(chat_id, 1)
    if last_message == []:
        return None
    else:
        return last_message[0][1]


def user_is_banned(id):
    global conn, cur
    cur.execute("""SELECT is_banned FROM users WHERE id = %s;""", (id,))
    answer = cur.fetchone()
    if answer == None:
        return False
    else:
        return answer[0]


def get_messages(chat_id, limit, offset=0):
    global conn, cur
    cur.execute("""SELECT user_main_id, body, created_at, is_read FROM messages WHERE chat_id = %s
                ORDER BY created_at DESC
                LIMIT %s OFFSET %s;""",
                (chat_id, limit, offset))
    return cur.fetchall()


def get_chat_by_users(user_main_id, user_chatter_id):
    global conn, cur
    cur.execute("""SELECT id FROM chats WHERE 
            (user_main_id = %s AND user_chatter_id = %s) OR 
            (user_chatter_id = %s AND user_main_id = %s)""",
                (user_main_id, user_chatter_id, user_main_id, user_chatter_id))
    chat_id = cur.fetchone()
    if chat_id == None:
        return None
    else:
        return chat_id[0]


def reset_chat_id_sequence():
    global conn, cur

    cur.execute("""SELECT setval(
    pg_get_serial_sequence('chats', 'id'),
    COALESCE(MAX(id), 1))
    FROM chats;
    """)

    conn.commit()


def reset_messages_id_sequence():
    global conn, cur

    cur.execute("""SELECT setval(
    pg_get_serial_sequence('messages', 'id'),
    COALESCE(MAX(id), 1))
    FROM messages;
    """)

    conn.commit()


def set_all_messages_is_read(id):
    global conn, cur

    cur.execute("""UPDATE messages SET is_read = True WHERE chat_id = %s;""", (id,))
    conn.commit()


def set_message_is_read(id):
    global conn, cur

    cur.execute("""UPDATE messages SET is_read = True WHERE id = %s;""", (id,))
    conn.commit()


def get_first_message(id):
    global conn, cur

    cur.execute("""SELECT id FROM messages WHERE chat_id = %s 
                ORDER BY created_at DESC
                LIMIT 1""", (id,))
    return cur.fetchone()[0]


def set_messages_read_in_chat(chat_id, current_user_id):
    """
    Отмечает все сообщения в чате, где получатель - current_user_id,
    как прочитанные. Возвращает список ID отправителей, чьи сообщения были прочитаны.
    """
    global conn, cur
    cur.execute("""
        SELECT DISTINCT m.user_main_id
        FROM messages m
        JOIN chats c ON m.chat_id = c.id
        WHERE m.chat_id = %s
          AND m.is_read = False
          AND (
            (c.user_main_id = %s AND m.user_main_id = c.user_chatter_id) OR
            (c.user_chatter_id = %s AND m.user_main_id = c.user_main_id)
          )
    """, (chat_id, current_user_id, current_user_id))
    senders = [row[0] for row in cur.fetchall()]

    cur.execute("""
        UPDATE messages
        SET is_read = True
        FROM chats
        WHERE messages.chat_id = %s
          AND messages.is_read = False
          AND (
            (chats.user_main_id = %s AND messages.user_main_id = chats.user_chatter_id) OR
            (chats.user_chatter_id = %s AND messages.user_main_id = chats.user_main_id)
          )
    """, (chat_id, current_user_id, current_user_id))
    conn.commit()
    return senders
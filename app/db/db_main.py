from psycopg import connect

from app.db.db_manager import (create_db, createTables,
                               add_user, get_user_attribute_by_login,
                               get_users_by_query, switch_to_test_env,
                               is_users_empty, add_test_data,
                               change_attribute_by_id, get_user_by_id,
                               chat_is_exists, create_chat, track_message,
                               track_message_and_create_chat, get_user_chats,
                               get_messages, user_is_banned)


def db_init():
    createTables()






db_init()
#create_db()
#add_user( "vovan", "krutoi_chel", "1234", "something")
# print(get_user_attribute_by_login("vovan", "id"))
# print(user_exists("kozol"))
#print(get_users_by_query('v', 5, 5, offset=0))
#print(get_user_by_id(1))
#change_attribute_by_id(4, "about", "hey guys welcome to my minecraft letsplay")
#print(chat_is_exists(1))
#print(create_chat(1, 1))
#track_message(1, 1, "bruh")
#print(track_message_and_create_chat(1, 1, "asdrftrsx"))
#print(get_user_chats(1, 10))
#print(get_messages(1,1, 10))
#add_test_users()
#print(user_is_banned(1))
#print(set_is_banned(1, False))
from app.db.db_manager import (create_db, createTables,
                               add_user, get_user_attribute_by_login,
                               get_user_attribute_list_by_login)


def db_init():
    create_db()
    createTables()

#db_init()
#add_user( "vovan", "krutoi_chel", "1234", "something")
# print(get_user_attribute_by_login("vovan", "id"))
# print(user_exists("kozol"))
print(get_user_attribute_list_by_login('ova', 'id', 5))

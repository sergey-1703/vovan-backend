from app.db.db_manager import (create_db, createTables,
                               add_user, get_user_attribute_by_login,
                               get_users_by_query, switch_to_test_env,
                               is_users_empty, add_test_users,
                               change_attribute_by_id, get_user_by_id)


def db_init():
    create_db()
    createTables()



if __name__ == "__main__":
    switch_to_test_env()

#db_init()
#add_user( "vovan", "krutoi_chel", "1234", "something")
# print(get_user_attribute_by_login("vovan", "id"))
# print(user_exists("kozol"))
print(get_users_by_query('v', 5, 5, offset=0))
#print(get_user_by_id(1))
#change_attribute_by_id(4, "about", "hey guys welcome to my minecraft letsplay")


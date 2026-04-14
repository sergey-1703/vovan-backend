from app.db.db_manager import create_db, createTables, add_user, get_user_by_login, user_exists


def db_init():
    create_db()
    createTables()

#db_init()
print(add_user( "vasya", "krutoi_chel", "1234", "something"))

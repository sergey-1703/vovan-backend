from app.db.db_manager import create_db, createTables, add_user


def db_init():
    create_db()
    createTables()

db_init()
add_user( "vovan", "krutoi_chel", "1234", "something")
from app.db.db_manager import create_db, createTables


def db_init():
    create_db()
    createTables()

# if __name__ == "__main__":
#     main()
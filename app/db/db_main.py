from db_manager import create_db, createTables


def main():
    create_db()
    createTables()

if __name__ == "__main__":
    main()
from src.utils.databaseManager import DatabaseManager

def create_database():
    db_manager = DatabaseManager()
    db_manager.connect()
    db_manager.createTables()
    db_manager.close()

if __name__ == "__main__":
    create_database() 

    
import sys, logging
sys.path.append(r'C:\Users\renan\Documents\Python\MusicSuite')

import utilities_db
from config_db import config

LOG = logging.getLogger()
LOG.setLevel("INFO")


def create_db_table():
    database_name = input("Enter Database Name: ")
    table_name = input("Enter Table Name: ")

    if not database_name or not table_name:
        print("Please enter both database name and table name.")
        return

    try:
        # Create the database
        utilities_db.create_database(host, user, password, database_name)

        # Connect to the database
        connection = utilities_db.create_connection(host, user, password, database_name)

        # Create the table
        utilities_db.create_table(connection, table_name)
        connection.close()

        print(f"Table '{table_name}' created in database '{database_name}'.")
    except Exception as e:
        LOG.error("An error occurred:", exc_info=True)
        print("Error creating table:", str(e))


if __name__ == "__main__":
    host = config["database"]["mysql_host"]
    user = config["database"]["mysql_user"]
    password = config["database"]["mysql_password"]
    create_db_table()

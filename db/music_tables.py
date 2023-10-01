import logging
from utilities_db import create_connection, create_database
from config import config

LOG = logging.getLogger()


def create_music_tables(environment):
    if not environment:
        print("Please enter the database name: ")
        return

    database_name = "music_" + environment

    try:

        # Create database
        create_database(host, user, password, database_name)

        # Connect to the database
        connection = create_connection(host, user, password, database_name)

        # Create Expenses Dimension Table
        create_songs_table_query = """
            CREATE TABLE IF NOT EXISTS songs (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                remix VARCHAR(255) NULL,
                genre VARCHAR(255),
                key_song VARCHAR(5),
                camelot VARCHAR(3),
                bpm INT,
                label VARCHAR(255),
                duration TIME,
                remixer VARCHAR(255) NULL,
                album VARCHAR(255),
                rating VARCHAR(5) NULL,
                date_added DATE
            )
        """
        with connection.cursor() as cursor:
            cursor.execute(create_songs_table_query)

        # Create Expenses Dimension Table
        create_sets_table_query = """
                CREATE TABLE IF NOT EXISTS sets (
                    id VARCHAR(36) PRIMARY KEY,
                    name VARCHAR(255),
                    bpm_range VARCHAR(10),
                    date DATE,
                    first_key VARCHAR(3),
                    first_camelot VARCHAR(3),
                    last_key VARCHAR(3),
                    last_camelot VARCHAR(3),
                    songs TEXT
                )
            """

        with connection.cursor() as cursor:
            cursor.execute(create_sets_table_query)

        connection.close()
        print("Tables and procedures created successfully.")
    except Exception as e:
        LOG.error("An error occurred:", exc_info=True)
        print("Error creating tables and procedures:", str(e))


if __name__ == "__main__":
    host = config["database"]["mysql_host"]
    user = config["database"]["mysql_user"]
    password = config["database"]["mysql_password"]
    environment = input("Enter the environment name: ")
    create_music_tables(environment)

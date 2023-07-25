import mysql.connector
from config_db import config

database_name = "MusicDB"
host = config["database"]["mysql_host"]
user = config["database"]["mysql_user"]
password = config["database"]["mysql_password"]


def create_connection():
    # Configure the connection to MySQL Server
    connection = mysql.connector.connect(host=host,
                                         user=user,
                                         password=password,
                                         database=database_name)
    return connection


def create_database(connection):
    # Use the provided connection to create the database
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
    cursor = connection.cursor()
    cursor.execute(create_database_query)
    cursor.close()
    connection.commit()


def create_table(connection, table_name):
    # Create a new table if it does not exist yet
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        ID VARCHAR(36) PRIMARY KEY,
        Order INT,
        Title VARCHAR(255),
        Artist VARCHAR(255),
        Genre VARCHAR(255),
        BPM INT,
        Key VARCHAR(5),
        Rating FLOAT,
        Bitrate INT,
        Album_Artist VARCHAR(255),
        Comments TEXT,
        Date_Added DATE
    );
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    cursor.close()
    connection.commit()


def delete_table(connection, table_name):
    # Delete the specified table if it exists
    delete_table_query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    cursor = connection.cursor()
    cursor.execute(delete_table_query)
    cursor.close()
    connection.commit()

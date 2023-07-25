import mysql.connector
from tests.db.config_db_test import config


def create_connection(host, user, password, database_name):
    # Configure the connection to MySQL Server
    connection = mysql.connector.connect(host=host,
                                         user=user,
                                         password=password,
                                         database=database_name)
    return connection


def create_database(host, user, password, database_name):
    # Configure the connection to MySQL Server
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )

    # Use the provided connection to create the database
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
    cursor = connection.cursor()
    cursor.execute(create_database_query)
    cursor.close()
    connection.commit()

    return connection


def delete_database(connection):
    # Extract the database name from the connection object
    database_name = connection.database

    # Delete the database if it exists
    delete_database_query = f"DROP DATABASE IF EXISTS {database_name};"
    cursor = connection.cursor()
    cursor.execute(delete_database_query)
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


def insert_data(connection, data_frame, table_name):
    # Convert the Pandas DataFrame to a list of tuples for data insertion
    data_to_insert = [tuple(row) for row in data_frame.values]

    # Insert data into the table
    insert_data_query = f"""
    INSERT INTO {table_name} (ID, Order, Title, Artist, Genre, BPM, Key, Rating, Bitrate, Album_Artist, Comments, Date_Added)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    cursor.executemany(insert_data_query, data_to_insert)
    connection.commit()
    cursor.close()


def delete_table(connection, table_name):
    # Delete the specified table if it exists
    delete_table_query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    cursor = connection.cursor()
    cursor.execute(delete_table_query)
    cursor.close()
    connection.commit()

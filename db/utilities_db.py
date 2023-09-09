import mysql.connector, sys
sys.path.append(r'C:\Users\renan\Documents\Python\MusicSuite')

from db.config_db import config
import logging

LOG = logging.getLogger()
LOG.setLevel("INFO")

# Default Value
QUERY_CREATE = config["query"]["songs_table"]
QUERY_INSERT = config["query"]["songs_insert"]


def create_connection(host, user, password, database_name):
    try:
        # Configure the connection to MySQL Server
        connection = mysql.connector.connect(host=host,
                                             user=user,
                                             password=password,
                                             database=database_name)
        LOG.info("Connection successful.")
        return connection
    except mysql.connector.Error as err:
        LOG.error(f"Failed to connect to MySQL Server: {err}")
        raise


def create_database(host, user, password, database_name):
    try:
        # Configure the connection to MySQL Server
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        LOG.info("Connection successful.")

        # Use the provided connection to create the database
        create_database_query = f"CREATE DATABASE IF NOT EXISTS {database_name};"
        LOG.info(f"Database creation query: {create_database_query}")

        cursor = connection.cursor()
        cursor.execute(create_database_query)
        cursor.close()
        connection.commit()
        LOG.info("Database created successfully.")
    except mysql.connector.Error as err:
        LOG.error(f"Failed to create database: {err}")
        raise


def delete_database(connection):
    try:
        # Extract the database name from the connection object
        database_name = connection.database

        # Delete the database if it exists
        delete_database_query = f"DROP DATABASE IF EXISTS {database_name};"
        LOG.info(f"Database deletion query: {delete_database_query}")

        cursor = connection.cursor()
        cursor.execute(delete_database_query)
        cursor.close()
        connection.commit()
        LOG.info("Database deleted successfully.")
    except mysql.connector.Error as err:
        LOG.error(f"Failed to delete database: {err}")
        raise


def create_table(connection, table_name, query=QUERY_CREATE):
    # Create a new table if it does not exist yet
    create_table_query = query.format(table_name)
    cursor = connection.cursor()

    try:
        cursor.execute(create_table_query)
        connection.commit()
        LOG.info(f"Table {table_name} created successfully.")
    except mysql.connector.Error as err:
        LOG.error(f"Failed to create table: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def insert_data(connection, data_frame, table_name, query=QUERY_INSERT):
    # Convert the Pandas DataFrame to a list of tuples for data insertion
    data_to_insert = [tuple(row) for row in data_frame.values]

    # Insert data into the table
    insert_data_query = query.format(table_name)
    cursor = connection.cursor()

    try:
        cursor.executemany(insert_data_query, data_to_insert)
        connection.commit()
        LOG.info(f"Data inserted into table {table_name} successfully.")
    except mysql.connector.Error as err:
        LOG.error(f"Failed to insert data into table: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()


def delete_table(connection, table_name):
    # Delete the specified table if it exists
    delete_table_query = f"""
    DROP TABLE IF EXISTS {table_name};
    """
    cursor = connection.cursor()

    try:
        cursor.execute(delete_table_query)
        connection.commit()
        LOG.info(f"Table {table_name} deleted successfully.")
    except mysql.connector.Error as err:
        LOG.error(f"Failed to delete table: {err}")
        connection.rollback()
        raise
    finally:
        cursor.close()

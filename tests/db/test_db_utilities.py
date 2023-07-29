import mysql.connector
import pandas as pd
import pytest
from db.utilities_db import *

database_name = "MusicDB_Test"
host = config["database"]["mysql_host"]
user = config["database"]["mysql_user"]
password = config["database"]["mysql_password"]


# Test create_database function
def test_create_database():
    create_database(host, user, password, database_name)

    connection_db = mysql.connector.connect(host=host, user=user, password=password)
    cursor = connection_db.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchall()
    cursor.close()
    connection_db.close()

    assert len(result) == 1


# Fixture to set up and tear down the database connection for each test
@pytest.fixture
def connection():
    connection = create_connection(host, user, password, database_name)
    yield connection
    connection.close()


# Test create_table function
def test_create_table(connection):
    table_name = "your_table_test"
    create_table(connection, table_name)
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchall()
    assert len(result) == 1
    cursor.close()


# Test insert_data function
def test_insert_data(connection):
    table_name = "your_table_test"  # Test table name
    data = {
        "id": ["id1", "id2"],
        "song_order": [1, 2],
        "name": ["Song 1", "Song 2"],
        "artist": ["Artist 1", "Artist 2"],
        "remix": ["Remix 1", "Remix 2"],
        "genre": ["Genre 1", "Genre 2"],
        "key_song": ["C", "D"],
        "bpm": [120, 130],
        "label": ["Label 1", "Label 2"],
        "time": ["12:22", "13:30"],  # Corrected Time format
        "remixer": ["Sigmahz", "Sigmahz"],
        "album": ["Album 1", "Album 2"],
        "rating": [4.5, 3.8],
        "date_added": ["2023-07-24", "2023-07-25"]
    }

    df = pd.DataFrame(data)
    create_table(connection, table_name)
    insert_data(connection, df, table_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()
    assert result[0] == len(data["id"])
    cursor.close()


# Test delete_table function
def test_delete_table(connection):
    table_name = "your_table_test"  # Test table name
    delete_table(connection, table_name)
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
    result = cursor.fetchall()
    assert len(result) == 0
    cursor.close()


# Test delete_database function
def test_delete_database(connection):
    delete_database(connection)
    cursor = connection.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchall()
    assert len(result) == 0
    cursor.close()

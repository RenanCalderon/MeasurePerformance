from db.utilities import *
import pytest

# Fixture to set up and tear down the database connection for each test
@pytest.fixture
def connection():
    connection = create_connection()
    yield connection
    connection.close()


# Test create_connection function
def test_create_connection():
    connection = create_connection()
    assert connection.is_connected()
    connection.close()


# Test create_database function
def test_create_database(connection):
    database_name = "MusicDB_Test"
    create_database(connection)
    cursor = connection.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchall()
    assert len(result) == 1
    cursor.close()


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
    import pandas as pd

    table_name = "your_table_test"  # Test table name
    data = {
        "ID": ["id1", "id2"],
        "Order": [1, 2],
        "Title": ["Song 1", "Song 2"],
        "Artist": ["Artist 1", "Artist 2"],
        "Genre": ["Genre 1", "Genre 2"],
        "BPM": [120, 130],
        "Key": ["C", "D"],
        "Rating": [4.5, 3.8],
        "Bitrate": [320, 256],
        "Album_Artist": ["Album Artist 1", "Album Artist 2"],
        "Comments": ["Comment 1", "Comment 2"],
        "Date_Added": ["2023-07-24", "2023-07-25"]
    }

    df = pd.DataFrame(data)
    create_table(connection, table_name)
    insert_data(connection, df, table_name)
    cursor = connection.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()
    assert result[0] == len(data["ID"])
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
    database_name = "MusicDB_Test"  # Test database name
    delete_database(connection)
    cursor = connection.cursor()
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchall()
    assert len(result) == 0
    cursor.close()
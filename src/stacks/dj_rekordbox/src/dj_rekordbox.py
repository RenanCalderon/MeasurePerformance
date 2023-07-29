import csv, logging
import pandas as pd
import uuid
import hashlib
from src.stacks.dj_rekordbox.src import camelot_circle
from src.stacks.dj_rekordbox.src.config_dj_rk import expected_column_names

LOG = logging.getLogger()
LOG.setLevel("INFO")


def read_file_to_dataframe(file_path):
    """
    Read a file with utf-16 encoding, construct a DataFrame, and use the first row as column titles.

    Args:
        file_path (str): Path of the CSV file.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-16') as archivo:
            lector = csv.reader(archivo, delimiter='\t')
            data = [fila for fila in lector]

        # Extract the titles from the first row
        titles = data[0]

        # Check if the column names match the expected ones
        mismatched_columns = [col for col in expected_column_names if col not in titles]

        if mismatched_columns:
            LOG.warning(f"The file {file_path} has different column names. Missing columns: {mismatched_columns}")

        # Convert the rest of the data into a DataFrame
        df_data = data[1:]  # Exclude the first row as it contains titles
        df = pd.DataFrame(df_data, columns=titles)

        # Remove the 'Artwork' column from the DataFrame
        if 'Artwork' in df.columns:
            df.drop('Artwork', axis=1, inplace=True)

        # Rename columns using the mapping dictionary
        df.rename(columns=expected_column_names, inplace=True)

        # Add camelot circle column
        camelot_circle.add_camelot_key_column(df, df["key_song"])

        # Combine the values of the desired columns into a single string
        df["Combined"] = df["name"] + df["artist"] + df["genre"] + df["remix"] + df["key_song"] + df["bpm"]

        # Apply a hash function (SHA-256) to generate the ID
        df["id"] = df["Combined"].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

        # Drop the "Combined" column if not needed
        df.drop(columns=["Combined"], inplace=True)

        LOG.info("DataFrame successfully generated.")
        return df

    except FileNotFoundError as e:
        LOG.error(f"File not found: {file_path}")
        raise e

    except Exception as e:
        LOG.error(f"An error occurred while reading the file: {file_path}")
        raise e

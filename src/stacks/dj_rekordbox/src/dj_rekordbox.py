import csv, logging
import pandas as pd
import numpy as np
import uuid
from src.stacks.dj_rekordbox.src import camelot_circle
from src.stacks.dj_rekordbox.src.config_dj_rk import expected_column_names
from src.log_config import LOG


def assign_rating_reference(rating_str):
    num_asterisks = rating_str.count('*')

    if num_asterisks == 0:
        return 0
    elif num_asterisks == 1:
        return 1
    elif num_asterisks == 2:
        return 2
    elif num_asterisks == 3:
        return 3
    elif num_asterisks == 4:
        return 4
    elif num_asterisks == 5:
        return 5
    else:
        return None


def generate_uuid_from_list(data_list):
    data_to_hash = ''.join(map(str, data_list))
    generated_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, data_to_hash)

    return str(generated_uuid)


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

        df['duration'] = pd.to_datetime(df['duration'], format='%M:%S').dt.time

        # Combine the values of the desired columns into a single string
        df["Combined"] = df[["name", "artist", "genre", "remix", "key_song", "bpm"]].agg(''.join, axis=1)

        # Apply a hash function (SHA-256) to generate the ID
        df["id"] = np.vectorize(generate_uuid_from_list)(df["Combined"].values)

        # Drop the "Combined" column if not needed
        df.drop(columns=["Combined"], axis=1, inplace=True)

        df["rating"] = df["rating"].apply(assign_rating_reference)

        df['song_order'] = pd.to_numeric(df['song_order'], errors='coerce')

        LOG.info("DataFrame successfully generated.")
        return df

    except FileNotFoundError as e:
        LOG.error(f"File not found: {file_path}")
        raise e

    except Exception as e:
        LOG.error(f"An error occurred while reading the file: {file_path}")
        raise e


def sets_dataframe(elements, keys, songs):
    column_names = ["name", "bpm_range", "date", "first_key", "first_camelot", "last_key", "last_camelot"]
    elements_df = pd.DataFrame(elements)
    elements_df = elements_df.T
    keys_df = pd.DataFrame(keys)
    keys_df = keys_df.T
    df = pd.concat([elements_df, keys_df], axis=1)
    df.columns = column_names
    df["songs"] = [songs] * len(df)

    # Combine the values of the desired columns into a single string
    df["Combined"] = df[["name", "bpm_range", "date"]].agg(''.join, axis=1)
    df["id"] = np.vectorize(generate_uuid_from_list)(df["Combined"].values)

    df = df[['id'] + column_names + ['songs']]

    return df

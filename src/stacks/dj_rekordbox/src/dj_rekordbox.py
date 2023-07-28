import csv
import pandas as pd
import uuid
from src.stacks.dj_rekordbox.src import camelot_circle
from config_dj_rk import config

input_folder = config["directory"]["input_folder"]
output_folder = config["directory"]["output_folder"]

# Variable se obtiene del usuario
file_name = 'Organic_House.txt'
file = input_folder + file_name


def read_csv_to_dataframe(file_path, file_output=False):
    """
    Read a CSV file with utf-16 encoding, construct a DataFrame, and use the first row as column titles.

    Args:
        file_path (str): Path of the CSV file.
        file_output (bool): Flag to indicate whether to save the DataFrame to a file.

    Returns:
        pandas.DataFrame: DataFrame containing the data from the CSV file.
    """
    with open(file_path, 'r', encoding='utf-16') as archivo:
        lector = csv.reader(archivo, delimiter='\t')
        data = [fila for fila in lector]

    # Extract the titles from the first row
    titles = data[0]

    # Convert the rest of the data into a DataFrame
    df_data = data[1:]  # Exclude the first row as it contains titles
    df = pd.DataFrame(df_data, columns=titles)
    column_mapping = {
        "#": "Order",
        "Título de la pista": "Title",
        "Artista": "Artist",
        "Género": "Genre",
        "BPM": "BPM",
        "Tonalidad": "Key",
        "Puntuación": "Rating",
        "Velocidad de bits": "Bitrate",
        "Artista del álbum": "Album_Artist",
        "Comentarios": "Comments",
        "Fecha añadida": "Date_Added",
    }

    df = df.rename(columns=column_mapping)
    camelot_circle.add_camelot_key_column(df, df["Key"])

    # Generate the ID column using UUID
    df["ID"] = [str(uuid.uuid4()) for _ in range(len(df))]

    if file_output:
        output_file_path = output_folder + file_name
        df.to_csv(output_file_path, index=False, sep='\t', encoding='utf-16')

    return df


df = read_csv_to_dataframe(file, file_output=True)
print(df)

import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QWidget, QPushButton
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt
from src.stacks.dj_rekordbox.src.dj_rekordbox import read_file_to_dataframe, sets_dataframe
from db.utilities_db import create_connection, insert_data
from db.config_db import column_orders
from config import config
from db.config_db import config as config_db
from src.log_config import LOG

ENVIRONMENT = config.get('environment')
DATABASE_NAME = config["database"]["music_database"]
HOST = config["database"]["mysql_host"]
USER = config["database"]["mysql_user"]
PASSWORD = config["database"]["mysql_password"]
QUERY_SONGS = config_db["query"]["songs_insert"]
QUERY_SETS = config_db["query"]["sets_insert"]


class DjRekordboxWindow(QMainWindow):
    def __init__(self, directory):
        super().__init__()

        # Window configuration
        self.setWindowTitle("Dj/Rekordbox Functionality")
        self.setGeometry(100, 100, 300, 200)

        # Create a central widget for the window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Button for saving Dj Set
        btn_save_dj_set = QPushButton("Save DJ Set", self)
        btn_save_dj_set.clicked.connect(self.save_dj_set)
        btn_save_dj_set.setStyleSheet("color: white; font-weight: bold; font-size: 14px; background-color: #2C2C2C;")

        # Add more buttons and functionalities here as needed

        # Window layout configuration
        layout = QGridLayout()
        layout.addWidget(btn_save_dj_set, 0, 0)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.selected_directory = directory

    def save_dj_set(self):
        # Get a list of all files in the selected directory
        files = os.listdir(self.selected_directory)

        for file_name in files:
            elements = file_name.split(".")[0].split("_")
            file_path = os.path.join(self.selected_directory, file_name)

            # Implement functionality to process each file here
            LOG.info(f"Processing file: {file_path}")
            df = read_file_to_dataframe(file_path)
            df = df.reindex(columns=column_orders)

            df_sorted = df.sort_values(by='song_order')

            first_element = df_sorted.iloc[0]
            last_element = df_sorted.iloc[-1]

            keys = [first_element['key_song'], first_element['camelot'],
                    last_element['key_song'], last_element['camelot']]

            songs = df_sorted[['song_order', 'id']].set_index('song_order').to_dict(orient='dict')['id']
            songs = str(songs)

            df_sets = sets_dataframe(elements, keys, songs)
            df_songs = df.drop('song_order', axis=1)

            # # Load Songs and Sets into the DB Music Suite
            connection = create_connection(HOST, USER, PASSWORD, DATABASE_NAME)
            insert_data(connection, df_songs, "songs", QUERY_SONGS)
            insert_data(connection, df_sets, "sets", QUERY_SETS)
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Application theme configuration
    app_palette = QPalette()
    app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    app_palette.setColor(QPalette.WindowText, QColor(Qt.white))
    app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # Add more color configurations as needed
    app.setPalette(app_palette)

    # Load a custom font if desired
    app_font = QFont("Arial", 10)
    app.setFont(app_font)

    window = DjRekordboxWindow()
    window.show()
    sys.exit(app.exec_())

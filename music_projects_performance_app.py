import os
import sys
import logging as LOG

import pandas as pd

from src.utilities import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout, QWidget, QListWidget, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

DEFAULT_DIRECTORY = r"C:\Users\renan\Documents\Ableton\Projects"
COLUMN_NAMES = ["Name", "Key", "Stage", "Date"]

# Configuración de logging
LOG.basicConfig(filename='tests/app_logs/app.log', level=LOG.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.setWindowTitle("Performance Analyzer")
        self.setGeometry(100, 100, 800, 600)

        # File list widget
        self.list_widget = QListWidget(self)

        # Folder path text field
        self.folder_edit = QLineEdit(self)
        self.folder_edit.setReadOnly(True)
        self.folder_edit.setFocusPolicy(Qt.NoFocus)

        # Select folder button
        btn_select_folder = QPushButton("Select Folder", self)
        btn_select_folder.clicked.connect(self.select_folder)
        btn_select_folder.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")

        # Analyze button
        btn_analyze = QPushButton("Performance Analysis", self)
        btn_analyze.clicked.connect(self.analyze_files)
        btn_analyze.setStyleSheet("color: black; font-weight: bold; font-size: 14px;")

        # Window layout configuration
        layout = QVBoxLayout()
        layout.addWidget(self.folder_edit)
        layout.addWidget(btn_select_folder)
        layout.addWidget(self.list_widget)
        layout.addWidget(btn_analyze)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_folder(self):
        directory_selected = QFileDialog.getExistingDirectory(self, "Select Folder", DEFAULT_DIRECTORY)
        if directory_selected:
            self.folder_edit.setText(directory_selected)
            self.list_files(directory_selected)

    def list_files(self, folder):
        self.list_widget.clear()
        files = os.listdir(folder)
        sorted_files = sorted(files, key=lambda x: os.path.splitext(x)[1])
        self.list_widget.addItems(sorted_files)
        LOG.info("Listed files in folder: {}".format(folder))

    def analyze_files(self):
        folder = self.folder_edit.text()
        als_files = [file for file in os.listdir(folder) if file.endswith(".als")]
        if als_files:
            LOG.info("Performing analysis on files...")
            df = pd.DataFrame()
            for file in als_files:
                sets = list_to_dataframe(parse_file(file), column_names=COLUMN_NAMES)
                df = pd.concat([df, sets])

            # Convertir la columna 'Fecha' al formato datetime
            df['Date_Format'] = pd.to_datetime(df['Date'])
            # Order data frame
            df_sorted = df.sort_values('Date_Format')

            LOG.info(f"DataFrame::: {df_sorted}")
            QMessageBox.information(self, "Selected Files", "\n".join(als_files))
        else:
            LOG.warning("No .als files found in the selected folder.")
            QMessageBox.warning(self, "No Files Found", "No .als files found in the selected folder.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Dark application theme
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(palette.Window, Qt.black)
    palette.setColor(palette.WindowText, Qt.white)
    palette.setColor(palette.Base, Qt.darkGray)
    palette.setColor(palette.Button, Qt.darkGray)
    palette.setColor(palette.ButtonText, Qt.white)
    app.setPalette(palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

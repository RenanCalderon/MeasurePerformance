import sys, logging, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

LOG = logging.getLogger()
LOG.setLevel("INFO")


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
            file_path = os.path.join(self.selected_directory, file_name)

            # Implement functionality to process each file here
            LOG.info("Processing file:", file_path)

        # Close the Dj/Rekordbox Window after processing the files
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

import sys, traceback, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QPushButton, QFileDialog, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QPalette

from src.stacks.music_performance import MusicPerformance
from src.stacks.folder_manager import FolderManager
from src.stacks.dj_rekordbox.dj_rekordbox_app import DjRekordboxWindow
from src.stacks.ableton.ableton_app import AbletonWindow
from src.log_config import setup_logger
from config.config import config

ENVIRONMENT = config.get('environment')
ABLETON_DIRECTORY = config.get('directory').get('ableton_projects')
SETS_DIRECTORY = config.get('directory').get('dj_sets')

log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.log')
LOG = setup_logger(log_file)
os.environ['LOG'] = log_file

LOG.info(f"Environment: {ENVIRONMENT}")
LOG.info(f"Ableton Directory: {ABLETON_DIRECTORY}")
LOG.info(f"Sets Directory: {SETS_DIRECTORY}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.setWindowTitle(f"Music {ENVIRONMENT}")
        self.setGeometry(100, 100, 800, 600)

        # Set dark application theme
        app_palette = QPalette()
        app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        app_palette.setColor(QPalette.WindowText, Qt.white)
        app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        app_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        app_palette.setColor(QPalette.ToolTipBase, Qt.white)
        app_palette.setColor(QPalette.ToolTipText, Qt.white)
        app_palette.setColor(QPalette.Text, Qt.white)
        app_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        app_palette.setColor(QPalette.ButtonText, Qt.white)
        app_palette.setColor(QPalette.BrightText, Qt.red)
        app_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        app_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        app_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(app_palette)

        # Set custom font for the title
        QFont("Arial", 24, QFont.Bold)

        # Set the title font and style
        self.setStyleSheet("QMainWindow::title { font-family: 'Arial'; font-size: 24px; font-weight: bold; color: black; }")

        # Button for Spotify
        btn_spotify = QPushButton("Spotify", self)
        btn_spotify.clicked.connect(self.open_spotify)
        btn_spotify.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Button for Music Performance
        btn_music_performance = QPushButton("Music Performance", self)
        btn_music_performance.clicked.connect(self.open_music_performance)
        btn_music_performance.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Button for Folder Manager
        btn_folder_manager = QPushButton("Folder Manager", self)
        btn_folder_manager.clicked.connect(self.open_folder_manager)
        btn_folder_manager.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Button for Music Analysis
        btn_music_analysis = QPushButton("Music Analysis", self)
        btn_music_analysis.clicked.connect(self.open_music_analysis)
        btn_music_analysis.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Button for Dj/Rekordbox
        btn_dj_rekordbox = QPushButton("Dj/Rekordbox", self)
        btn_dj_rekordbox.clicked.connect(self.open_dj_rekordbox)
        btn_dj_rekordbox.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Button for Ableton
        btn_ableton = QPushButton("Ableton", self)
        btn_ableton.clicked.connect(self.open_ableton)
        btn_ableton.setStyleSheet("color: white; font-weight: bold; font-size: 18px; background-color: #2C2C2C;")

        # Window layout configuration
        layout = QGridLayout()
        layout.addWidget(btn_spotify, 0, 0)
        layout.addWidget(btn_music_performance, 0, 1)
        layout.addWidget(btn_folder_manager, 1, 0)
        layout.addWidget(btn_music_analysis, 1, 1)
        layout.addWidget(btn_dj_rekordbox, 2, 0)
        layout.addWidget(btn_ableton, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Adjust button sizes to match the available space
        self.adjust_button_sizes()

    def adjust_button_sizes(self):
        # Get the available space in the main window
        main_width = self.centralWidget().width()
        main_height = self.centralWidget().height()

        # Calculate the button width and height
        button_width = main_width // 2
        button_height = main_height // 2

        # Set the button sizes
        for button in self.centralWidget().findChildren(QPushButton):
            button.setFixedSize(button_width, button_height)

    def open_spotify(self):
        print("Spotify functionality")

    def open_music_performance(self):
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Folder", ABLETON_DIRECTORY)
        if folder_selected:
            folder_edit = QLineEdit(folder_selected)
            music_performance = MusicPerformance(folder_edit)
            music_performance.start_performance()

    def open_folder_manager(self):
        print("Folder Manager functionality")
        # Rename File
        folder_selected = QFileDialog.getExistingDirectory(self, "Select Folder", ABLETON_DIRECTORY)
        if folder_selected:
            folder_manager = FolderManager(folder_selected)
            folder_manager.rename_als_files()

    def open_music_analysis(self):
        print("Music Analysis functionality")

    def open_dj_rekordbox(self):
        print("Dj/Rekordbox functionality")
        self.dj_window = DjRekordboxWindow(SETS_DIRECTORY)
        self.dj_window.show()

    def open_ableton(self):
        print("Ableton functionality")
        self.ableton_window = AbletonWindow(ABLETON_DIRECTORY)
        self.ableton_window.show()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()
        LOG.info(f"Music Suite APP Initiated")
        app.exec_()
    except Exception as e:
        traceback.print_exc()

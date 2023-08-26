import sys, logging, subprocess, traceback
from src.stacks.ableton.src.ableton_utilities import get_latest_als_file
from config import config
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QWidget, QPushButton, QFileDialog, QMessageBox, QListWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt

LOG = logging.getLogger()
LOG.setLevel("INFO")
ABLETON_PATH = config.get("ableton_config").get("exe_path")


class AbletonWindow(QMainWindow):
    def __init__(self, directory):
        super().__init__()

        # Window configuration
        self.setWindowTitle("Ableton Functionality")
        self.setGeometry(100, 100, 300, 200)

        # Create a central widget for the window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Button for saving Dj Set
        btn_open_project = QPushButton("Open Project", self)
        btn_open_project.clicked.connect(self.open_project)
        btn_open_project.setStyleSheet("color: white; font-weight: bold; font-size: 14px; background-color: #2C2C2C;")

        # Add more buttons and functionalities here as needed

        # Window layout configuration
        layout = QGridLayout()
        layout.addWidget(btn_open_project, 0, 0)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.selected_directory = directory

    def open_project(self):
        project = QFileDialog.getExistingDirectory(self, "Select Project Directory", self.selected_directory)

        if not project:
            LOG.info("No project directory selected.")
            return

        latest_files = get_latest_als_file(project)

        if latest_files:
            if len(latest_files) > 1:
                # If more than one project has the same date
                self.select_project_dialog(latest_files)

            else:
                try:
                    subprocess.run([ABLETON_PATH, latest_files[0]])
                except OSError as e:
                    print("Error:", e)

    def select_project_dialog(self, files):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Select Project")
        dialog.setText(" ")

        # Remove default label and create a custom QLabel
        label = QLabel("Multiple projects found with the same date. Please select a project:")
        label.setAlignment(Qt.AlignCenter)  # Center-align the label
        label.setStyleSheet("color: black; font-weight: bold;")  # Customize label style
        dialog.layout().addWidget(label)

        list_widget = QListWidget()

        # Apply styles to the list widget
        list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #000000;
                    color: #FFFFFF;
                    border: 1px solid #FFFFFF;
                    font-size: 14px;
                }
                QListWidget::item {
                    padding: 10px;
                }
                QListWidget::item:selected {
                    background-color: #2C2C2C;
                    color: #FFFFFF;
                }
            """)

        dialog.layout().addWidget(list_widget)
        list_widget.addItems(files)

        ok_button = dialog.addButton("Open", QMessageBox.AcceptRole)
        cancel_button = dialog.addButton(QMessageBox.Cancel)

        # Apply styles to the buttons
        ok_button.setStyleSheet("""
                    color: #000000;
                    font-size: 14px;
                """)
        cancel_button.setStyleSheet("""
                    color: #000000;
                    font-size: 14px;
                """)

        dialog.setLayout(QVBoxLayout())  # Set the layout to QVBoxLayout
        dialog.layout().addWidget(list_widget)  # Add the list widget to the layout

        # Create a container for the buttons with a QHBoxLayout
        buttons_container = QWidget()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(ok_button)
        buttons_layout.setAlignment(Qt.AlignRight)  # Align buttons to the right
        buttons_container.setLayout(buttons_layout)
        dialog.layout().addWidget(buttons_container)

        dialog.exec_()

        if dialog.clickedButton() == ok_button:
            selected_project = list_widget.currentItem().text()
            try:
                subprocess.run([ABLETON_PATH, selected_project])
            except OSError as e:
                print("Error:", e)
        elif dialog.clickedButton() == cancel_button:
            dialog.close()


if __name__ == "__main__":
    try:
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

        window = AbletonWindow()
        window.show()
        LOG.info("Ableton functionality executed successfully")
        sys.exit(app.exec_())

    except Exception as e:
        LOG.error("Error executing Ableton functionality")
        traceback.print_exc()

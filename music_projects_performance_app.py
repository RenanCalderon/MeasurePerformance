import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QMessageBox, QVBoxLayout,
                             QWidget, QListWidget, QPushButton, QLineEdit)
from PyQt5.QtCore import Qt

DEFAULT_DIRECTORY = r"C:\Users\renan\Documents\Ableton\Projects"

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

    def analyze_files(self):
        selected_files = [item.text() for item in self.list_widget.selectedItems()]
        if selected_files:
            QMessageBox.information(self, "Selected Files", "\n".join(selected_files))
        else:
            QMessageBox.warning(self, "No Files Selected", "Please select at least one file.")

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

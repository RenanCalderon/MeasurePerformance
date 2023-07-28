import sys, logging
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, \
    QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QColor, QPalette

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
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog

        # Configuración del estilo para los botones
        style_sheet = "QPushButton { color: white; font-weight: bold; font-size: 14px; background-color: #2C2C2C; }"

        file_name, _ = QFileDialog.getSaveFileName(self, "Save DJ Set", self.selected_directory,
                                                   "Text Files (*.txt);;All Files (*)",
                                                   options=options)

        if file_name:
            # Implement functionality to save DJ Set here using the selected file_name
            print("Saving DJ Set to:", file_name)

        # Close the DjRekordboxWindow after saving the DJ Set
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Configuración del tema de la aplicación
    app_palette = QPalette()
    app_palette.setColor(QPalette.Window, QColor(53, 53, 53))
    app_palette.setColor(QPalette.WindowText, Qt.white)
    app_palette.setColor(QPalette.Base, QColor(25, 25, 25))
    # Agrega más configuraciones de colores según sea necesario
    app.setPalette(app_palette)

    # Cargar una fuente personalizada si se desea
    app_font = QFont("Arial", 10)
    app.setFont(app_font)

    window = DjRekordboxWindow()
    window.show()
    sys.exit(app.exec_())
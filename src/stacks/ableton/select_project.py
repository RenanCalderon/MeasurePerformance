from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QApplication


class SelectProjectDialog(QDialog):
    def __init__(self, files):
        super().__init__()

        self.setWindowTitle("Select Project")
        self.setLayout(QVBoxLayout())

        self.list_widget = QListWidget()
        self.list_widget.addItems(files)

        # Apply styles to the list widget
        self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #000000;
                    font-size: 14px;
                }
                QListWidget::item {
                    padding: 5px;
                }
                QListWidget::item:selected {
                    background-color: #2C2C2C;
                    color: #FFFFFF;
                }
            """)

        self.layout().addWidget(self.list_widget)

        self.ok_button = QPushButton("Open Selected Project")
        self.ok_button.clicked.connect(self.accept)
        self.layout().addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.layout().addWidget(self.cancel_button)


if __name__ == "__main__":
    app = QApplication([])

    files = ["Project 1", "Project 2", "Project 3"]
    dialog = SelectProjectDialog(files)
    if dialog.exec_() == QDialog.Accepted:
        selected_project = dialog.list_widget.currentItem().text()
        print("Selected Project:", selected_project)

    app.exec_()

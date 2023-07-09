from PyQt5.QtWidgets import (QDialog, QLabel, QVBoxLayout)


class ReportDialog(QDialog):
    def __init__(self, report_text):
        super().__init__()

        layout = QVBoxLayout()
        label = QLabel(report_text)
        layout.addWidget(label)

        self.setLayout(layout)
        self.setWindowTitle("Analysis Report")
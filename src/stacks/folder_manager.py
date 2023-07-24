import os
import glob
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt


class RenameALSDialog(QDialog):
    def __init__(self, current_name, parent=None):
        super().__init__(parent)
        self.current_name = current_name

        layout = QVBoxLayout()

        # Show the current ALS file name using QLabel
        label = QLabel(f"Current ALS file name: {self.current_name}")
        layout.addWidget(label)

        # Input fields for prefix, suffix, and new name
        self.prefix_edit = QLineEdit()
        self.suffix_edit = QLineEdit()
        self.new_name_edit = QLineEdit()
        layout.addWidget(self.prefix_edit)
        layout.addWidget(self.suffix_edit)
        layout.addWidget(self.new_name_edit)

        # OK and Cancel buttons aligned in a row
        button_box = QDialogButtonBox()
        button_box.setOrientation(Qt.Horizontal)
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        self.ok_button.setStyleSheet("background-color: #3a3a3a; color: white;")
        self.cancel_button.setStyleSheet("background-color: #3a3a3a; color: white;")
        button_box.addButton(self.ok_button, QDialogButtonBox.AcceptRole)
        button_box.addButton(self.cancel_button, QDialogButtonBox.RejectRole)
        layout.addWidget(button_box)

        self.setLayout(layout)
        self.setWindowTitle("Rename ALS Files")

    def get_user_input(self):
        prefix = self.prefix_edit.text()
        suffix = self.suffix_edit.text()
        new_name = self.new_name_edit.text()
        return prefix, suffix, new_name


class FolderManager:
    def __init__(self, working_directory):
        self.working_directory = working_directory

    def get_latest_als_file(self):
        als_files = glob.glob(os.path.join(self.working_directory, "*.als"))
        if als_files:
            return max(als_files, key=os.path.getctime)
        else:
            return None

    def rename_als_files(self):
        latest_als_file = self.get_latest_als_file()
        if latest_als_file:
            # Get the current ALS file name without the full path
            current_name = os.path.basename(latest_als_file)

            # Show the custom dialog with the current ALS file name
            dialog = RenameALSDialog(current_name)
            if dialog.exec_():
                # Get the new prefix, suffix, and new name from the dialog
                prefix, suffix, new_name = dialog.get_user_input()

                folder_path = os.path.dirname(latest_als_file)
                for file in os.listdir(folder_path):
                    if file.endswith(".als"):
                        old_file_path = os.path.join(folder_path, file)

                        # Extract the date part from the current name (separated by "_")
                        date_part = file.split("_")[-1].replace(".als", "")

                        new_file_name = f"{prefix}{date_part}_{new_name}_{suffix}.als"
                        new_file_path = os.path.join(folder_path, new_file_name)
                        os.rename(old_file_path, new_file_path)
                print("Renaming completed.")
            else:
                print("Operation canceled.")
        else:
            print("No .als files found in the selected folder.")


if __name__ == "__main__":
    pass

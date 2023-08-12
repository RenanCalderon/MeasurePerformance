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

        # Input fields for Name, Key, and Stage
        label_name = QLabel("Name:")
        self.name_edit = QLineEdit()
        self.name_edit.setStyleSheet("color: black;")  # Set text color to black
        layout.addWidget(label_name)
        layout.addWidget(self.name_edit)

        label_key = QLabel("Key:")
        self.key_edit = QLineEdit()
        self.key_edit.setStyleSheet("color: black;")  # Set text color to black
        layout.addWidget(label_key)
        layout.addWidget(self.key_edit)

        label_stage = QLabel("Stage:")
        self.stage_edit = QLineEdit()
        self.stage_edit.setStyleSheet("color: black;")  # Set text color to black
        layout.addWidget(label_stage)
        layout.addWidget(self.stage_edit)

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
        self.setWindowTitle("Rename Project")

        # Connect the cancel button to the reject slot to cancel the operation
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_user_input(self):
        name = self.name_edit.text()
        key = self.key_edit.text()
        stage = self.stage_edit.text()
        return name, key, stage


class FolderManager:
    def __init__(self, working_directory):
        self.working_directory = working_directory

    def get_latest_als_file(self):
        als_files = glob.glob(os.path.join(self.working_directory, "*.als"))
        if als_files:
            return max(als_files, key=os.path.getctime)
        else:
            print("No ALS files found")
            return None

    def rename_als_files(self):
        latest_als_file = self.get_latest_als_file()
        if latest_als_file:
            # Get the current ALS file name without the full path
            current_name = os.path.basename(latest_als_file)

            # Show the custom dialog with the current ALS file name
            dialog = RenameALSDialog(current_name)
            if dialog.exec_():
                # Get the new name, key, and stage from the dialog
                name, key, stage = dialog.get_user_input()

                # Rename the folder with the Name and Key
                new_folder_name = f"{name}_{key} Project"

                new_folder_path = os.path.join(os.path.dirname(self.working_directory), new_folder_name)
                os.rename(self.working_directory, new_folder_path)
                print(f"Folder renamed to: {new_folder_name}")

                # Update the working_directory attribute to the new folder path
                self.working_directory = new_folder_path

                for file in os.listdir(self.working_directory):
                    if file.endswith(".als"):
                        old_file_path = os.path.join(self.working_directory, file)

                        # Extract the date part from the current name (separated by "_")
                        date_part = file.split("_")[-1].replace(".als", "")

                        # Create the new file name with the parameters and the original date
                        new_file_name = f"{name}_{key}_{stage}_{date_part}.als"
                        new_file_path = os.path.join(self.working_directory, new_file_name)
                        os.rename(old_file_path, new_file_path)
                print("Renaming completed.")
            else:
                print("Operation canceled.")
        else:
            print("No .als files found in the selected folder.")


if __name__ == "__main__":
    pass

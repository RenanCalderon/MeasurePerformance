import os
import pandas as pd
from src.utilities import list_to_dataframe, parse_file, days_track, days_stages
from src.report_dialog import ReportDialog
from PyQt5.QtWidgets import QMessageBox

DEFAULT_DIRECTORY = r"C:\Users\renan\Documents\Ableton\Projects"
COLUMN_NAMES = ["name", "key", "stage", "date"]


class MusicPerformance:
    def __init__(self, folder_edit):
        self.folder_edit = folder_edit
        print("Music Performance functionality")

    def start_performance(self):
        folder = self.folder_edit.text()
        als_files = [file for file in os.listdir(folder) if file.endswith(".als")]
        if als_files:
            print("Performing analysis on files...")
            df = pd.DataFrame()
            for file in als_files:
                sets = list_to_dataframe(parse_file(file), column_names=COLUMN_NAMES)
                df = pd.concat([df, sets])

            # Convert column 'Date' to datetime & order data frame
            df['datetime'] = pd.to_datetime(df['date'])
            df = df.sort_values('datetime')
            df['date_diff'] = df['datetime'].diff()
            print(f"DataFrame::: {df}")

            # Measure the days
            days = days_track(df["datetime"])
            stage_totals = days_stages(df)

            # Create the report
            report_text = f"Days on the project: {days} \nDay expended per Stage: {stage_totals}"
            report_dialog = ReportDialog(report_text)
            report_dialog.exec_()

        else:
            print("No .als files found in the selected folder.")
            QMessageBox.warning(self, "No Files Found", "No .als files found in the selected folder.")

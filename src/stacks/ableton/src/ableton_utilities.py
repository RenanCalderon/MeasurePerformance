import glob, os, logging
from collections import defaultdict
from src.log_config import LOG


def get_latest_als_file(project, file_type="als"):

    end = ["*.als"]
    if file_type != "als":
        end = ["*.wav", "*.mp3"]

    files = []
    file_dates = defaultdict(list)
    for options in end:
        files.extend(glob.glob(os.path.join(project, options)))

    if files:
        for file in files:
            file_date = os.path.basename(file).split("_")[-1].split(".")[0]
            file_dates[file_date].append(file)
        LOG.info(f"Dictionary: {file_dates}")

        latest_date = max(file_dates.keys())
        latest_files = file_dates[latest_date]
        LOG.info(f"Latest Files: {latest_files}")

        return latest_files
    else:
        LOG.warning(f"No {file_type} files found")
        return None

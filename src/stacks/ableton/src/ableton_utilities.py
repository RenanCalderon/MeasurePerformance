import glob, os, logging
from collections import defaultdict

LOG = logging.getLogger()
LOG.setLevel("INFO")


def get_latest_als_file(project):
    als_files = glob.glob(os.path.join(project, "*.als"))
    file_dates = defaultdict(list)

    if als_files:
        for als_file in als_files:
            file_date = os.path.basename(als_file).split("_")[-1].split(".")[0]
            file_dates[file_date].append(als_file)
        # LOG.info(f"Dictionary: {file_dates}")

        latest_date = max(file_dates.keys())
        latest_files = file_dates[latest_date]
        LOG.info(f"Latest Files: {latest_files}")

        return latest_files
    else:
        print("No ALS files found")
        return None

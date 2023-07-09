import logging
import pandas as pd

LOG = logging.getLogger()
LOG.setLevel('INFO')


def parse_file(name_file):
    '''
    :param name_file: name of the file to parse
    :return: A list of each element
    '''

    file = name_file.replace(".", "_")
    parse = file.split("_")[:-1]

    return parse


def list_to_dataframe(data_list, column_names=None):
    '''
    :param data_list: List of elements to convert
    :param column_names: Insert the names of the columns
    :return: A data frame
    '''
    if column_names:
        df = pd.DataFrame([data_list], columns=column_names)
    else:
        df = pd.DataFrame([data_list])
    return df


def days_track(dates):
    total_days = (dates.diff() / pd.Timedelta(days=1)).fillna(0).sum()
    # n_days = (dates.max() - dates.min()).days
    LOG.info(f"Days on the project: {total_days} days")
    return total_days


def days_stages(df):
    # Measure the days between stages on the proyect
    stage_days = df.groupby('stage')['datetime'].diff() / pd.Timedelta(days=1)
    stage_days = stage_days.fillna(1)
    stage_totals = stage_days.groupby(df['stage']).sum()
    LOG.info(f"stages days: {stage_totals}")
    return stage_totals

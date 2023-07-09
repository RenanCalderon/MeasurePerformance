import pandas as pd


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

# def stage(scan):
#     Prod = []
#     Mix = []
#     Mast = []
#
#     for file in scan:
#         if 'Prod' in file:
#             Prod.append(file)
#         elif 'Mix' in file:
#             Mix.append(file)
#         else:
#             Mast.append(file)
#
#     print(f"Production files \n {Prod}")
#     print(f"Mixing files \n {Mix}")
#     print(f"Master files \n {Mast}")
#
#     return Prod, Mix, Mast

# Prod, Mix, Mast = stage(scanner)




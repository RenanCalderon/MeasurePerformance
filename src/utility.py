from datetime import datetime

DATE_FORMAT = "%Y%m%d"


def parse_file(name_file):
    '''
    :param name_file: name of the file to parse
    :return: A list of each element
    '''

    file = name_file.replace(".", "_")
    list = file.split("_")

    return list


# for file in
# parse_file(Prod[1], 'type')


def stage(scan):
    Prod = []
    Mix = []
    Mast = []

    for file in scan:
        if 'Prod' in file:
            Prod.append(file)
        elif 'Mix' in file:
            Mix.append(file)
        else:
            Mast.append(file)

    print(f"Production files \n {Prod}")
    print(f"Mixing files \n {Mix}")
    print(f"Master files \n {Mast}")

    return Prod, Mix, Mast

# Prod, Mix, Mast = stage(scanner)




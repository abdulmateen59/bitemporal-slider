from src import ColumnName
from src import logger


def read_data(filename: str, path: str = './') -> dict[str, list[str]]:
    """
    Read file line by line and saves it in defined data structure

    :param filename: Name of the file.
    :param path: path where the file is stored, default is current directory

    :return: complete dataset
    """

    data: dict[str, list[str]] = {ColumnName.SYSTEM.value: [],
                                  ColumnName.VALID.value: [],
                                  ColumnName.DATA.value: []}
    try:
        with open(f'{path}{filename}', 'r') as csv_file:
            for line in csv_file.readlines()[1:]:
                system, valid, value = line.split(",", 3)
                data[ColumnName.SYSTEM.value].append(system)
                data[ColumnName.VALID.value].append(valid)
                data[ColumnName.DATA.value].append(value.strip('\n'))
        return data
    except IOError as E:
        logger.error(f"{type(E)}: {E}")


def write_result(output: list[list[str | float]],
                 filename: str,
                 path: str = './') -> None:
    """
    Writes results to file based

    :param output: Calculated data to be written
    :param filename: Name of the file.
    :param path: path where the file is stored, default is current directory
    """
    try:
        with open(f'{path}{filename}.csv', "w") as file:
            for row in output:
                file.write(f'{str(row[0])} {str(row[1])} {str(row[2])}' + '\n')
    except IOError as E:
        logger.error(f"{type(E)}: {E}")

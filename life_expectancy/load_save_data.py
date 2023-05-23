"""
Functions to read and load data
"""
from inspect import getsourcefile
from os.path import dirname, abspath, join
import pandas as pd

def __get_current_directory_full_path() -> str:
    """
    Returns the absolute path of the directory containing the current 
    Python file.
    :return: A string representing the absolute path of the directory 
    containing the current Python file.
    """
    current_file_path: str = abspath(getsourcefile(lambda: 0))
    current_dir_path: str = dirname(current_file_path)

    return current_dir_path

def load_data(path: str = None) -> pd.DataFrame:
    """
    Loads the 'eu_life_expectancy_raw.tsv' data file from the 'data' folder
    :return: Pandas dataframe with data
    :raises FileNotFoundError: If the 'eu_life_expectancy_raw.tsv' file cannot
     be found.
    """
    if not path:
        path = join(
            __get_current_directory_full_path(),
            "data",
            "eu_life_expectancy_raw.tsv"
        )
    data = pd.read_csv(path, sep='\t')
    return data

def save_data(data: pd.DataFrame) -> None:
    """
    Data is saved to a CSV file named 'pt_life_expectancy.csv' in the 'data'
    folder.
    :param data: Pandas Dataframe with the cleaned data
    :return: 
    """
    path = join(
        __get_current_directory_full_path(),
        "data",
        "pt_life_expectancy.csv"
    )
    data.to_csv(path, index = False)

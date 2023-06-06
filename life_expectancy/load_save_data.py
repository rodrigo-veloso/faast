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

class DataLoader():
    """
    This class is responsible for verifying the path and format
    and assign the right load method
    """

    def __init__(self, path: str = None, file_format: str = 'csv'):
        self.path = path
        self.__check_path()
        self.file_format = file_format
        self.__configs = {
            'csv': {
                'method': pd.read_csv,
                'kwargs': {'sep':'\t'}
            },
            'json': {
                'method': pd.read_json,
                'kwargs': {'orient': 'records'}
            }
        }

    def __check_path(self) -> None:
        """
        check if a path was passed, if it didn't, reads from default path
        """
        if not self.path:
            self.path = join(
                __get_current_directory_full_path(),
                "data",
                "eu_life_expectancy_raw.tsv"
            )

    def load(self) -> pd.DataFrame:
        """
        Loads data from a given file in a give path with a given format

        :param path: str, path to the data file
        :param format: str, file format, it can be json or csv like

        :return: Pandas dataframe with data
        """
        configs = self.__configs[self.file_format]
        loader = configs['method']
        kwargs = configs['kwargs']
        return loader(self.path, **kwargs)

def load_data(path: str = None, file_format: str = None) -> pd.DataFrame:
    """
    Calls load from the DataLoader
    :param path: str, path to the data file
    :param format: str, file format, it can be json or csv like

    :return: Pandas dataframe with data
    """
    return DataLoader(path, file_format).load()

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

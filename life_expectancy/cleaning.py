"""
Assignment 1
"""
from inspect import getsourcefile
from os.path import dirname, abspath, join
import argparse
import numpy as np
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

def load_data() -> pd.DataFrame:
    """
    Loads the 'eu_life_expectancy_raw.tsv' data file from the 'data' folder
    :return: Pandas dataframe with data
    :raises FileNotFoundError: If the 'eu_life_expectancy_raw.tsv' file cannot
     be found.
    """
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
    :param data: 
    :return: 
    """
    path = join(
        __get_current_directory_full_path(),
        "data",
        "pt_life_expectancy.csv"
    )
    data.to_csv(path, index = False)

def clean_data(data: pd.DataFrame, country: str = 'PT') -> pd.DataFrame:
    """
    Cleans and transforms the input wide_data to a long format.

    The input raw_data should have the following columns:
    - unit,sex,age,geo\\time: A mixed column with the variables unit, sex, age,
     and region separated by commas.
    - One column for each year of data.

    The function performs the following steps:
    - Splits the mixed column into separate columns and sets them as the first
    columns of the data frame.
    - Transforms the raw_data from a wide format to a long format with columns
    'year' and 'value'.
    - Converts the 'year' and 'value' columns to numeric data types and drops
    rows with missing values.
    - Selects the rows corresponding to the specified country_code.

    :param wide_data: A pandas DataFrame containing the data to be cleaned and
    transformed.
    :param country_code: A string representing the country code of the country
    to be selected.
    :return: A pandas DataFrame containing the cleaned and transformed data.
    """
    life_expectancy = data

    id_variables = ['unit','sex','age','region']

    life_expectancy[id_variables] = (
        life_expectancy['unit,sex,age,geo\\time'].str.split(',', expand = True)
    )
    life_expectancy = life_expectancy.drop(columns=['unit,sex,age,geo\\time'])
    life_expectancy = life_expectancy[life_expectancy["region"] == country]

    years = [column for column in life_expectancy.columns if column not in id_variables]
    life_expectancy = pd.melt(
        life_expectancy,
        value_vars = years,
        id_vars = ['unit','sex','age','region'],
        var_name = 'year',
        value_name = 'value',
    )
    life_expectancy['year'] = (
        life_expectancy['year']
        .str.replace(" ", "")
        .astype(int)
    )
    life_expectancy['value'] = (
        life_expectancy['value']
        .str.replace(" ", "")
        .str.replace("e", "")
        .replace(":",np.nan)
        .astype(float)
    )

    life_expectancy = life_expectancy.dropna()

    return life_expectancy

def main(country = 'PT') -> None:
    """
    Calls load data, clean data and save data
    :param country_code: A string representing the country code of the country
    to be selected.
    :return:
    """
    life_expectancy_data = load_data()
    life_expectancy_data = clean_data(life_expectancy_data, country)
    save_data(life_expectancy_data)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean data and filter by country')
    parser.add_argument(
        '--country',
        type=str, default='PT',
        help='Country code to filter data'
    )
    args = parser.parse_args()

    main(args["country"])

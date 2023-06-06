"""
Functions to run the cleaning pipeline
"""
import argparse
from enum import Enum
from itertools import chain

import numpy as np
import pandas as pd
from life_expectancy.load_save_data import load_data, save_data

# Define possible countries
class Countries(Enum):
    """Existing regions in dataset"""
    AT = 'AUSTRIA'
    BE = 'BELGIUM'
    BG = 'BULGARIA'
    CH = 'SWITZERLAND'
    CY = 'CYPRUS'
    CZ = 'CZECHIA'
    DK = 'DENMARK'
    EE = 'ESTONIA'
    EL = 'GREECE'
    ES = 'SPAIN'
    FI = 'FINLAND'
    FR = 'FRANCE'
    HR = 'CROACIA'
    HU = 'HUNGARY'
    IS = 'ICELAND'
    IT = 'ITALY'
    LI = 'LIECHTENSTEIN'
    LT = 'LITHUANIA'
    LU = 'LUXEMBOURG'
    LV = 'LATVIA'
    MT = 'MALTA'
    NL = 'NETHERLANDS'
    NO = 'NORWAY'
    PL = 'POLAND'
    PT = 'PORTUGAL'
    RO = 'ROMANIA'
    SE = 'SWEDEN'
    SI = 'SLOVENIA'
    SK = 'SLOVAKIA'
    DE = 'GERMANY'
    AL = 'ALBANIA'
    IE = 'IRELAND'
    ME = 'MONTENEGRO'
    MK = 'NORTH_MACEDONIA'
    RS = 'SERBIA'
    AM = 'ARMENIA'
    AZ = 'AZERBAIJAN'
    GE = 'GEORGIA'
    TR = 'TURKEY'
    UA = 'UKRAINE'
    BY = 'BELARUS'
    UK = 'UNITED_KINGDOM'
    XK = 'KOSOVO'
    FX = 'FRANCE_METROPOLITAN'
    MD = 'MOLDOVA'
    SM = 'SAN_MARINO'
    RU = 'RUSSIA'

def get_conutries_list():
    """Return list of countries"""
    return [e.value for e in Countries]

class Regions(Enum):
    """Existing regions in dataset"""
    EU_27_2020 = 'EUROPEAN_UNION'
    DE_TOT = 'GERMANY_TOT'
    EA_18 = 'EURO_AREA_18'
    EA_19 = 'EURO_AREA_19'
    EFTA = 'EUROPE_FREE_TRADE_ASSOCIATION'
    EEA30_2007 = 'EUROPEAN_ECONOMIC_AREA_2007'
    EEA31 = 'EUROPEAN_ECONOMIC_AREA'
    EU27_2007 = 'EUROPEAN_UNION_2007'
    EU28 = 'EUROPEAN_UNION_28'

Regions = Enum('Regions', [(i.name, i.value) for i in chain(Countries, Regions)])
Regions.get_conutries_list = get_conutries_list

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
        .str.replace(r"[a-zA-Z\s]+", "")
        .replace(":",np.nan)
        .astype(float)
    )

    life_expectancy = life_expectancy.dropna()

    return life_expectancy

def main(country:str = 'Portugal', path:str = None, file_format:str = 'csv') -> None:
    """
    Calls load data, clean data and save data
    :param country_code: A string representing the country code of the country
    to be selected.
    :return:
    """

    # Verify if country is on the list of possible regions
    country = Regions(country.upper()).name

    life_expectancy_data = load_data(path, file_format)
    life_expectancy_data = clean_data(life_expectancy_data, country)
    save_data(life_expectancy_data)
    return life_expectancy_data

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean data and filter by country')
    parser.add_argument(
        '--country',
        type=str, default='Portugal',
        help='Country code to filter data'
    )
    parser.add_argument(
        '--path',
        type=str, default = None,
        help='path to where the data is stored'
    )
    parser.add_argument(
        '--file_format',
        type=str, default='csv',
        help='file format, e.g., json, csv'
    )
    args = parser.parse_args()

    main(
        args.country,
        args.path,
        args.file_format
    )

"""
Assignment 1
"""
import argparse
import numpy as np
import pandas as pd

def load_data():
    """
    load data from file
    """
    data = pd.read_csv('life_expectancy/data/eu_life_expectancy_raw.tsv', sep='\t')
    return data

def save_data(data):
    """
    save data to file
    """
    data.to_csv('life_expectancy/data/pt_life_expectancy.csv', index = False)

def clean_data(data, country = 'PT'):
    """
    Cleans data.
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
    life_expectancy['year'] = life_expectancy['year'].str.replace(" ", "")
    life_expectancy['year'] = life_expectancy['year'].astype(int)
    life_expectancy['value'] = life_expectancy['value'].str.replace(" ", "")
    life_expectancy['value'] = life_expectancy['value'].str.replace("e", "")
    life_expectancy['value'] = life_expectancy['value'].replace(":",np.nan)
    life_expectancy['value'] = life_expectancy['value'].astype(float)
    life_expectancy = life_expectancy.dropna()

    return life_expectancy

def main(country = 'PT'):
    """
    main function
    """
    life_expectancy_data = load_data()
    life_expectancy_data = clean_data(life_expectancy_data, country)
    save_data(life_expectancy_data)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean data and filter by country')
    parser.add_argument('--country', help='Country to use as filter')
    args = parser.parse_args()

    main(args["country"])

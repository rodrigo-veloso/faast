"""Tests for the cleaning module"""
from unittest import mock

import pandas as pd

from life_expectancy.cleaning import main, clean_data, Regions
from . import FIXTURES_DIR


def test_country_list(countries_list_expected):
    """Test get countries list from Regions class"""
    countries_list_actual = Regions.get_countries_list()

    assert not set(countries_list_actual) ^ set(countries_list_expected)

def test_clean_data(pt_life_expectancy_expected, eu_life_expectancy_input):
    """Run the `clean_data` function and compare the output to the expected output"""
    cleaned_data = clean_data(eu_life_expectancy_input.copy())
    pd.testing.assert_frame_equal(
        cleaned_data.reset_index(drop=True), pt_life_expectancy_expected
    )

def test_main(pt_life_expectancy_expected):
    """
    Run the `main` function and compare the output to the expected output
    """
    with mock.patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        mock_to_csv.side_effect = print("Message: Dataframe saved to CSV")
        cleaned_data = main(path = FIXTURES_DIR / "eu_life_expectancy_input.tsv")
        pd.testing.assert_frame_equal(
            cleaned_data.reset_index(drop=True), pt_life_expectancy_expected
        )

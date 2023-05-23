"""Tests for the load_save_data module"""
from unittest import mock

import pandas as pd

from life_expectancy.load_save_data import load_data, save_data
from . import FIXTURES_DIR


def test_load_data(eu_life_expectancy_input):
    """Test the load_data function to check if the actual input is the same of the expected input (fixture)"""
    pt_life_expectancy_input_actual = load_data(FIXTURES_DIR / "eu_life_expectancy_input.tsv" )
    pd.testing.assert_frame_equal(
        pt_life_expectancy_input_actual, eu_life_expectancy_input
    )

def test_save_data():
    """ Test the save_data function to check if the Dataframe is being saved to CSV"""
    with mock.patch.object(pd.DataFrame, "to_csv") as mock_to_csv:
        mock_to_csv.side_effect = print("Message: Dataframe saved to CSV")
        save_data(pd.DataFrame())
        mock_to_csv.assert_called_once()

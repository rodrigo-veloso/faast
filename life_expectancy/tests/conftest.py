"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")

@pytest.fixture(scope="session")
def eu_life_expectancy_input() -> pd.DataFrame:
    """Fixture to load the expected input, the raw file"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_input.tsv", sep='\t')

@pytest.fixture(scope="session")
def countries_list_expected() -> list:
    """Fixture to load the expected country list"""
    return [
        'AUSTRIA', 'BELGIUM', 'BULGARIA', 'SWITZERLAND', 'CYPRUS', 'CZECHIA', 'DENMARK',
        'ESTONIA', 'GREECE', 'SPAIN', 'FINLAND', 'FRANCE', 'CROACIA', 'HUNGARY', 
        'ICELAND', 'ITALY', 'LIECHTENSTEIN', 'LITHUANIA', 'LUXEMBOURG', 'LATVIA',
        'MALTA', 'NETHERLANDS', 'NORWAY', 'POLAND', 'PORTUGAL', 'ROMANIA', 'SWEDEN',
        'SLOVENIA', 'SLOVAKIA', 'GERMANY', 'ALBANIA', 'IRELAND', 'MONTENEGRO', 
        'NORTH_MACEDONIA', 'SERBIA', 'ARMENIA', 'AZERBAIJAN', 'GEORGIA', 'TURKEY',
        'UKRAINE', 'BELARUS', 'UNITED_KINGDOM', 'KOSOVO', 'FRANCE_METROPOLITAN',
        'MOLDOVA', 'SAN_MARINO', 'RUSSIA'
    ]

import pytest
import pandas as pd
import requests
import os
from const import DATA_DIR, DATE
from transformation import json_to_dataframe


@pytest.fixture()
def json_dataframe():
    try:
        return pd.read_json(os.path.join(DATA_DIR, f"exchange_rate_PLN_{DATE}.json"))
    except IOError:
        print('Cannot open json file')


def test_api_is_giving_200_status_code():
    ENDPOINT = 'https://open.er-api.com/v6/latest/PLN'
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_all_columns_are_in_the_dataframe(json_dataframe):
    expected = ['base_code', 'provider', 'documentation', 'rates', 'result', 'terms_of_use'
         'time_eol_unix', 'time_last_update_unix', 'time_last_update_utc', 'time_next_update_unix'
         'time_next_update_utc', 'terms_of_usetime_eol_unix', 'time_next_update_unixtime_next_update_utc'].sort()
    actual = json_dataframe.columns.to_list().sort()
    assert expected == actual


def test_json_to_dataframe(json_dataframe):
    expected = ['currency_code', 'provider', 'time_last_update_utc', 'rates'].sort()
    df_json = json_to_dataframe()
    actual = df_json.columns.to_list().sort()
    assert actual == expected

from prefect.testing.utilities import prefect_test_harness
from prefect import flow
import numpy as np
import pandas as pd
import pytest
from src.hourly_weather_update.tasks.format_GET_hourly_api_task import format_GET_hourly_api


raw_input = pd.read_csv("tests/fixtures/raw-weather-hourly.csv")
actual_dataframe = pd.read_csv("tests/fixtures/weather-hourly.csv")

# format date column of expected output
actual_dataframe["date"] = pd.to_datetime(
    actual_dataframe['date'], format="%Y-%m-%d")  # formats datetime

#######
# Test task 'format_GET_daily_api' from 'format_GET_daily_api_task' with test input
# compare results with expected output via. df assert
#######
def test_format_GET_hourly_api():
    pd.testing.assert_frame_equal(
        format_GET_hourly_api.fn(raw_input), actual_dataframe, check_dtype=False)


if __name__ == "__main__":
    test_format_GET_hourly_api()

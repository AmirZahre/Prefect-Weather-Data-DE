import time
from datetime import datetime
import pygeohash as gh
from prefect import task

import pandas as pd
# https://stackoverflow.com/questions/40136651/stack-output-with-all-individual-indexs-filled-in-pandas-dataframe
pd.set_option('display.multi_sparse', False)


@task
def format_GET_daily_api(raw_response_daily_df):

    # assert raw_response_daily_df is a DataFrame
    assert isinstance(raw_response_daily_df,
                      pd.DataFrame), "raw_response_daily_df should be a pandas DataFrame"

    response_daily_df = raw_response_daily_df.copy()  # create copy of raw df

    # hashes the long/lat values
    city_id = response_daily_df.apply(lambda x: gh.encode(
        x["latitude"], x["longitude"], precision=10), axis=1)

    # inserts the newly created geoash ID
    response_daily_df.insert(0, "city_id", city_id)

    # formats datetime
    response_daily_df["date"] = pd.to_datetime(
        response_daily_df['date'], format="%Y-%m-%d")

    # https://stackoverflow.com/questions/46375147/create-new-columns-from-unique-row-values-in-a-pandas-dataframe
    # https://stackoverflow.com/questions/26255671/pandas-column-values-to-columns
    # collapses df
    response_daily_df = response_daily_df.pivot_table(index=["city_id", "date"],
                                                      columns='parameter', values='value').reset_index()

    # remove index name
    response_daily_df = response_daily_df.rename_axis(
        None, axis=1)

    # Changing column values and lowercase
    response_daily_df.rename(
        columns=lambda s: s.replace(":", "_"), inplace=True)
    response_daily_df.columns = response_daily_df.columns.str.lower()

    # Changing data type for sunrise/sunset values
    # https://stackoverflow.com/questions/41783003/how-do-i-convert-timestamp-to-datetime-date-in-pandas-dataframe
    response_daily_df["sunrise_ux"] = [datetime.fromtimestamp(
        x) for x in response_daily_df["sunrise_ux"]]
    response_daily_df["sunset_ux"] = [datetime.fromtimestamp(
        x) for x in response_daily_df["sunset_ux"]]

    # create unique ID
    weather_id = response_daily_df.apply(lambda x: str(int(time.mktime(
        x["date"].timetuple()))) + x["city_id"], axis=1)  # hashes the long/lat values

    # inserts the newly created geoash ID
    response_daily_df.insert(0, "daily_weather_id", weather_id)

    # log of transformed df
    print(response_daily_df)

    return response_daily_df

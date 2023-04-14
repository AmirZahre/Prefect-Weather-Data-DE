import time

import pandas as pd
import pygeohash as gh
from prefect import task

# https://stackoverflow.com/questions/40136651/stack-output-with-all-individual-indexs-filled-in-pandas-dataframe
pd.set_option('display.multi_sparse', False)


@task
def format_GET_hourly_api(raw_response_hourly_df):
    # assert raw_response_hourly_df is a DataFrame
    assert isinstance(
        raw_response_hourly_df, pd.DataFrame
    ), "raw_response_hourly_df should be a pandas DataFrame"

    response_hourly_df = raw_response_hourly_df.copy()

    # hashes the long/lat values
    city_id = response_hourly_df.apply(
        lambda x: gh.encode(x["latitude"], x["longitude"], precision=10),
        axis=1,
    )

    # inserts the newly created geoash ID
    response_hourly_df.insert(0, "city_id", city_id)

    # formats datetime
    response_hourly_df["date"] = pd.to_datetime(
        response_hourly_df['date'], format="%Y-%m-%d"
    )

    # collapses df
    response_hourly_df = response_hourly_df.pivot_table(
        index=["city_id", "date"], columns='parameter', values='value'
    ).reset_index()

    # remove index name
    response_hourly_df = response_hourly_df.rename_axis(None, axis=1)

    # Changing column values and lowercase
    response_hourly_df.rename(
        columns=lambda s: s.replace(":", "_"), inplace=True
    )
    response_hourly_df.columns = response_hourly_df.columns.str.lower()

    # create unique ID
    # hashes the long/lat values
    weather_id = response_hourly_df.apply(
        lambda x: str(int(time.mktime(x["date"].timetuple()))) + x["city_id"],
        axis=1,
    )

    # inserts the newly created geoash ID
    response_hourly_df.insert(0, "hourly_weather_id", weather_id)

    # log of transformed df
    print(response_hourly_df)
    return response_hourly_df

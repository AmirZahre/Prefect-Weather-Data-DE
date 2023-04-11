from src.daily_weather_update.utils.db import WarehouseConnection
from src.daily_weather_update.utils.sde_config import get_warehouse_creds
from prefect.blocks.system import Secret
from datetime import date, datetime
from prefect import task
from requests.auth import HTTPBasicAuth
import requests
import pandas as pd
# https://stackoverflow.com/questions/40136651/stack-output-with-all-individual-indexs-filled-in-pandas-dataframe
pd.set_option('display.multi_sparse', False)


@task
def GET_daily_api():
    username = Secret.load("auth-weather-username").get()
    password = Secret.load("auth-weather-password").get()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
    daily = f"https://api.meteomatics.com/{now}-06:00/t_min_2m_24h:C,t_max_2m_24h:C,weather_code_24h:idx,precip_24h:mm,precip_type:idx,sunrise:ux,sunset:ux,t_mean_2m_24h:C/53.5462055,-113.491241+51.0460954,-114.065465/json?model=mix"

    # Making a get request
    response_daily = requests.get(daily,
                                  auth=HTTPBasicAuth(username, password))

    raw_response_daily_json = response_daily.json()['data']

    # normalize df
    raw_response_daily_df = pd.json_normalize(raw_response_daily_json, ['coordinates', 'dates'], [
                                              'parameter', ['coordinates', 'lat'], ['coordinates', 'lon']])

    # rename columns
    raw_response_daily_df.rename(columns={
                                 'coordinates.lat': 'latitude', 'coordinates.lon': 'longitude'}, inplace=True)

    WarehouseConnection(get_warehouse_creds()).insert_table(
        raw_response_daily_df, "raw_weather_daily")

    return raw_response_daily_df

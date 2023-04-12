from src.utils.db import WarehouseConnection
from src.utils.sde_config import get_warehouse_creds
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
    locations = "53.5462055,-113.491241+51.0460954,-114.065465+49.2608724,-123.113952+43.6534817,-79.3839347+40.7127281,-74.0060152+38.5810606,-121.493895+48.1371079,11.5753822+60.1674881,24.9427473+52.5170365,13.3888599+59.3251172,18.0710935+48.8534951,2.3483915"
    params = "t_min_2m_24h:C,t_max_2m_24h:C,weather_code_24h:idx,precip_24h:mm,precip_type:idx,sunrise:ux,sunset:ux,t_mean_2m_24h:C"
    period = f"{now}-06:00"
    daily_api_url = f"https://api.meteomatics.com/{period}/{params}/{locations}/json?model=mix"

    # Making a get request
    response_daily = requests.get(daily_api_url,
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

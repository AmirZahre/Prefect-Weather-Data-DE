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
def GET_hourly_api():
    username = Secret.load("auth-weather-username").get()
    password = Secret.load("auth-weather-password").get()
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000")
    hourly = f"https://api.meteomatics.com/{now}-06:00/t_2m:C,t_apparent:C,relative_humidity_2m:p,wind_speed_2m:bft,wind_dir_2m:d,weather_code_1h:idx/53.5462055,-113.491241+51.0460954,-114.065465+49.2608724,-123.113952+43.6534817,-79.3839347+40.7127281,-74.0060152+38.5810606,-121.493895+48.1371079,11.5753822+60.1674881,24.9427473+52.5170365,13.3888599+59.3251172,18.0710935+48.8534951,2.3483915/json?model=mix"

    # Making a get request
    response_hourly = requests.get(hourly,
                                   auth=HTTPBasicAuth(username, password))

    raw_response_hourly_json = response_hourly.json()['data']
    raw_response_hourly_df = pd.json_normalize(raw_response_hourly_json, ['coordinates', 'dates'], [
                                               'parameter', ['coordinates', 'lat'], ['coordinates', 'lon']])
    raw_response_hourly_df.rename(
        columns={'coordinates.lat': 'latitude', 'coordinates.lon': 'longitude'}, inplace=True)

    WarehouseConnection(get_warehouse_creds()).insert_table(
        raw_response_hourly_df, "raw_weather_hourly")

    return raw_response_hourly_df

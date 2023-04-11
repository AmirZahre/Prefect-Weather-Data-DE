from prefect import flow, task
from src.hourly_weather_update.utils.db import WarehouseConnection
from src.hourly_weather_update.utils.sde_config import get_warehouse_creds
from src.hourly_weather_update.tasks.GET_hourly_api_task import GET_hourly_api
from src.hourly_weather_update.tasks.format_GET_hourly_api_task import format_GET_hourly_api


@task
def upload_hourly_data(response_hourly_df):
    WarehouseConnection(get_warehouse_creds()).insert_table(
        response_hourly_df, "weather_hourly")


@flow(log_prints=True, name="GET_Hourly_Data")
def GET_hourly():

    # GET data from source. upload source (raw) data to raw_weather_hourly
    raw_data = GET_hourly_api.submit()
    formatted_data = format_GET_hourly_api.submit(
        raw_data)  # transform data to proper DataFrame
    upload_hourly_data.submit(formatted_data)  # upload to table weather_hourly


if __name__ == "__main__":
    GET_hourly()

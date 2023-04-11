from prefect import flow, task
from src.daily_weather_update.tasks.GET_daily_api_task import GET_daily_api
from src.daily_weather_update.tasks.format_GET_daily_api_task import format_GET_daily_api
from src.daily_weather_update.utils.db import WarehouseConnection
from src.daily_weather_update.utils.sde_config import get_warehouse_creds


@task  # upload the daily weather DataFrame to the weather_daily table
def upload_daily_data(response_daily_df):
    WarehouseConnection(get_warehouse_creds()).insert_table(
        response_daily_df, "weather_daily")


@flow(log_prints=True, name="GET_Daily_Data")
def GET_daily():
    # GET data from source. upload source (raw) data to raw_weather_daily
    raw_data = GET_daily_api.submit()
    formatted_data = format_GET_daily_api.submit(
        raw_data)  # transform data to proper DataFrame
    upload_daily_data.submit(formatted_data)  # upload to table weather_daily


if __name__ == "__main__":
    GET_daily()

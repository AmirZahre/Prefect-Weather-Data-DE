from prefect.deployments import Deployment
from src.daily_weather_update.weather_daily_etl import GET_daily


def main():
    deployment = Deployment.build_from_flow(
        flow=GET_daily,
        name="GET_Daily_Data_Deployment"
    )
    deployment.apply()


if __name__ == "__main__":
    main()

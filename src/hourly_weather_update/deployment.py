from prefect.deployments import Deployment

from src.hourly_weather_update.weather_hourly_etl import GET_hourly


def main():
    deployment = Deployment.build_from_flow(
        flow=GET_hourly, name="GET_Hourly_Data_Deployment"
    )
    deployment.apply()


if __name__ == "__main__":
    main()

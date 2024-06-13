
<br  />

<h2  align="center">Data Warehouse for Weather Data</h3>

  

<p  align="center">

This project extracts weather data from https://www.meteomatics.com/, performs several transformations, and then uploads to a relational database. Then, using the metabase container (http://localhost:3000), visualizations on the data can be performed, such as below.
  
![Screenshot from 2023-04-12 14-20-40](https://user-images.githubusercontent.com/71795488/231575573-9f3c5680-1def-45b3-b1e6-96be5f577302.png)



<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Setting Up The project](#setting-up-the-project)
- [About The Project](#about-the-project)
	- [Process](#process)
- [Warehouse Layout](#warehouse-layout)
- [Tables](#tables)
	- [Static](#static)
	- [Dynamic](#dynamic)

  
<!-- TO START -->
## Setting Up The project
Prior to recreating this project, you will need to create an account on https://www.meteomatics.com/ and retreive both your username and password. Save the two into individual Prefect Secret [Blocks](https://docs.prefect.io/latest/concepts/blocks/), naming them `auth-weather-username` and `auth-weather-password`, respectively.
<br>

Run these commands to setup your project locally.
```shell
# Clone the code as shown below
git clone https://github.com/AmirZahre/weather_prefect_etl
cd weather_prefect_etl
```
Create an .env file and populate the following variables:

```
WAREHOUSE_USER=user
WAREHOUSE_PASSWORD=password
WAREHOUSE_DB=warehouse
WAREHOUSE_HOST=warehouse
WAREHOUSE_PORT=5432

PREFECT_API_KEY=api_key
PREFECT_WS=workspace_id
```

Continue with the shell commands.
```shell
# Build containers & test
make up # Spin up the containers
make ci # Run CI tests (isort format lint pytest)

# Local run pipelines
make daily_etl
make hourly_etl

# OPTIONAL: Deploy pipelines (to deploy the flows onto Prefect Cloud)
make daily_etl_deploy
make hourly_etl_deploy

# OPTIONAL: Spin up Prefect agent (to run the deployed flows on Prefect Cloud)
make prefect_agent
```




<!-- ABOUT THE PROJECT -->

## About The Project

  

meteomatics provides a diverse portfolio of global weather data. This project is intended to retreive specific portions of this data via. API, transform the data to allow easier analysis, and then upload this data into a relational database for future retreival. Two tables are generated from the API: one that shows changing weather patterns on an hourly basis, and one for daily.

  

The Python library `requests` is used to retrieve the data. `pandas` is used to transform the data into sql-digestible DataFrames. The `SQLAlchemy`-backend `df.to_sql` is then used to upload the DataFrames to the RDS database.

  

### Process

  

1. The two flows within `src` contain the `Prefect` code that is ran every hour (for the hourly table) and daily (for the daily table).

2. The tasks called perform several functions:

	* The first set of tasks calls the API and retrieves the data. Some minor cleanup is performed here, specifically to collapse the .json data into a pandas DataFrame. A DataFrame is returned. This task is ran for each of those two tables.
		* The task names are: `GET_daily_api_task` and `GET_hourly_api_task`.

	* The second set of tasks retrieves the pandas DataFrame, and performs the bulk of the transformations needed to properly map the data to the respective database table. A DataFrame is returned. This task is ran for each of those two tables.
		* The task names are: `format_GET_daily_api_task` and `format_GET_hourly_api_task`.

3. The third task uploads the DataFrame to the respective database table. This task is located within each flow file, entitled either `upload_daily_data` or `upload_hourly_data` and is a python function wrapped with the task decorator.

<!-- Warehouse -->

## Warehouse Layout

  

  

![Screenshot from 2023-03-22 21-25-24](https://user-images.githubusercontent.com/71795488/227098906-70565eb2-95d2-4a35-a2c6-ab96d975f0ef.png)

There exists six tables: four dimension and two fact.

  

## Tables

### Fact

*  **Weather_Hourly**: Fed data hourly, this table contains attributes focused on the current temperature, humidity, and wind.

*  **Weather_Daily**: Fed data daily, this table is focused on aggregate weather observations of the day. This includes min/max/mean values for temperature, as well as sunset/sunrise times.



### Dimension  

*  **Country**: Contains data pertaining to the country name. This table is linked to the `City` table via. a one-to-many relationship of the `country_id` attribute.

*  **City**: Stores city details. Its primary key, `city_id`, is a geohash of its coordinates. It is linked to the table `Country` via. a many-to-one `country_id` attribute, and linked to `Weather_Hourly` and `Weather_Daily` via. a one-to-many relationship with its `city_id` attribute.

*  **Weather_Status**: Contains a mapping of weather status id's provided by the source API, converting them into a description of current weather. The id is the primary key, `weather_status_id`, and serves as a foreign key in both the `Weather_Hourly` and `Weather_Daily` tables.

*  **Precipitation_Type**: Similar mapping as `Weather_Status`, but for precipitation. It only serves the `Weather Daily` table.

include .env

up:
	docker compose --env-file .env up --build -d

down:
	docker compose --env-file .env down --volumes

### Daily Weather ETL
daily_etl:
	docker exec loader python3 src/daily_weather_update/weather_daily_etl.py

daily_etl_deploy:
	docker exec loader python3 src/daily_weather_update/deployment.py
###

### Hourly Weather ETL
hourly_etl:
	docker exec loader python3 src/hourly_weather_update/weather_hourly_etl.py

hourly_etl_deploy:
	docker exec loader python3 src/hourly_weather_update/deployment.py
###

prefect_agent:
	docker exec loader prefect agent start --pool default-agent-pool

pytest:
	docker exec loader pytest tests/

location:
	docker exec loader ls

##### initialize prefect cloud
prefect-cloud:
	docker exec loader prefect cloud login --key '${PREFECT_API_KEY}' --workspace '${PREFECT_WS}'
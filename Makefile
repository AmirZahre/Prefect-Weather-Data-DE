up:
	docker compose --env-file .env up --build -d

down:
	docker compose --env-file .env down

### Daily Weather ETL
daily_etl:
	docker exec loader python3 src/daily_weather_update/weather_daily_etl.py

daily_etl_deploy:
	docker exec loader python3 src/daily_weather_update/deployment.py

### Hourly Weather ETL
hourly_etl:
	docker exec loader python3 src/hourly_weather_update/weather_hourly_etl.py

hourly_etl_deploy:
	docker exec loader python3 src/hourly_weather_update/deployment.py

# Spin up Local Agent
prefect_agent:
	docker exec loader prefect agent start --pool default-agent-pool

# CI
format:
	docker exec loader python -m black -S --line-length 79 .

isort:
	docker exec loader isort .

pytest:
	docker exec loader pytest -p no:warnings tests 

lint: 
	docker exec loader flake8 /opt/sde

ci: isort format lint pytest
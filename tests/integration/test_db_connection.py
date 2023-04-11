from src.daily_weather_update.utils.db import WarehouseConnection
from src.daily_weather_update.utils.sde_config import get_warehouse_creds
import pytest

# test Postgres db connection
class TestDbConnection:
    def test_db_connection(self):
        with WarehouseConnection(get_warehouse_creds()).managed_cursor() as curr:
            # print('PostgreSQL database version:')
            curr.execute('SELECT version()')
            db_version = curr.fetchone()
            print(db_version)
            assert db_version is not None
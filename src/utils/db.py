from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2
from sqlalchemy import create_engine

@dataclass
class DBConnection:
    db: str
    user: str
    password: str
    host: str
    port: int = 5432


class WarehouseConnection:
    def __init__(self, db_conn: DBConnection):
        self.conn_url = (
            f'postgresql://{db_conn.user}:{db_conn.password}@'
            f'{db_conn.host}:{db_conn.port}/{db_conn.db}'
        )

    @contextmanager
    def managed_cursor(self, cursor_factory=None):
        self.conn = psycopg2.connect(self.conn_url)
        self.conn.autocommit = True
        self.curr = self.conn.cursor(cursor_factory=cursor_factory)
        try:
            yield self.curr
        finally:
            self.curr.close()
            self.conn.close()

    def insert_table(self, df, table, if_exists="append", test=False):
        engine = create_engine(self.conn_url)

        # try appending the DataFrame (df) to the respective Postgres table (table).
        # default param is append.
        try:
            df.to_sql(
                table,
                con=engine,
                index=False,
                if_exists='append'
            )
            
            print("to_sql() completed via. (sqlalchemy)")
        except Exception as e: print(e)
        finally:
            engine.dispose()
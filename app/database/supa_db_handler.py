import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

from interfaces.db_handler import DatabaseHandler


class SupaDatabaseHandler(DatabaseHandler):
    def __init__(self):
        load_dotenv()
        self._connection_string = os.getenv("DATABASE_URL")

        if not self._connection_string:
            raise RuntimeError("DATABASE_URL is missing")

    def query(self, sql: str):
        # Pyscopg connect is what connects to db with connection string
        # Row factory basically lets us return the info as an object that can be
        # indexed like a hash table instead of a tuple we'd have to do weird stuff with
        with psycopg.connect(
            self._connection_string,
            row_factory=dict_row,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

                if cur.description is not None:
                    return cur.fetchall()

                return None
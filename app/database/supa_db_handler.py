import os
import psycopg
from dotenv import load_dotenv
from interfaces.db_handler import DatabaseHandler

class SupaDatabaseHandler(DatabaseHandler):

    def __init__(self):
        load_dotenv()
        self._connection_string = os.getenv("DATABASE_URL")

    def query(self, sql: str):
        with psycopg.connect(self._connection_string) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

                if cur.description is not None:
                    return cur.fetchall()

                return None
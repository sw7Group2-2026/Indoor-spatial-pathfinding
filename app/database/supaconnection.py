import os
import psycopg
from dotenv import load_dotenv

# This basically connects to supabase(which is postgresql database) using an adapter called pscyopg which is popular adapter for python to postgres server
# conn cursor as cur allows us to run code on the database.
# For interesting docs check this: https://www.psycopg.org/psycopg3/docs/basic/usage.html

load_dotenv()

connection_string = os.getenv("DATABASE_URL")
with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user, now()")
        print("Connected:", cur.fetchone())
        cur.execute("SELECT extensions.postgis_full_version()")
        print(cur.fetchone()[0])
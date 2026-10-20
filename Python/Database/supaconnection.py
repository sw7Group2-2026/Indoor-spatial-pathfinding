import os
import psycopg
from urllib.parse import quote
from dotenv import load_dotenv

# This basically connects to supabase(which is postgresql database) using an adapter called pscyopg which is popular adapter for python to postgres server
# conn cursor as cur allows us to run code on the database.
# For interesting docs check this: https://www.psycopg.org/psycopg3/docs/basic/usage.html


load_dotenv()

host = os.environ["PGHOST"]
port = os.getenv("PGPORT")
database = quote(os.environ["PGDATABASE"], safe="")
user = quote(os.environ["PGUSER"], safe="")
password = quote(os.environ["PGPASSWORD"], safe="")
sslmode = "require"
connect_timeout = 15

# Encode user, password, and database so special characters work in the URL.
connection_string = (
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
    f"?sslmode={sslmode}&connect_timeout={connect_timeout}"
)

with psycopg.connect(connection_string) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT current_database(), current_user, now()")
        print("Connected:", cur.fetchone())
        cur.execute("SELECT extensions.postgis_full_version()")
        print(cur.fetchone()[0])
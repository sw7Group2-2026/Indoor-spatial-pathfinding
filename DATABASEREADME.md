## Connect to Supabase PostgreSQL and PostGIS

The project uses a hosted Supabase PostgreSQL database with the PostGIS extension. Python and pgAdmin connect to the same database.

I'm using docker here to run python. So this branch and the running of this code requires feature/DOCKER-SETUP to be pushed first.

### Configure environment variables

Create a `.env` file in the project root, beside `compose.yml` based on `.env.example`:

Get the exact connection details from Peter. As these can be confidential and can't be pushed to github.

### Install Python dependencies

Ensure `Python/requirements.txt` includes:

```text
psycopg
dotenv
```

Then rebuild:

```bash
docker compose build py
```

`urllib.parse` is included with Python and does not need to be installed.

### Enable PostGIS

This is only needed once per database. (I've already done it for our database)

In the Supabase dashboard:

1. Open **Database → Extensions**.
2. Enable **postgis**.
3. Select the **extensions** schema.

The other PostGIS extensions are not required for the initial DXF workflow.

### Test the database connection

Run the database connection file i've created for testing:

```bash
docker compose run --rm py python Database/supaconnection.py
```

Expected output includes:

```text
Connected: ('postgres', 'postgres', ...)
POSTGIS="3.3.7 ..." ...
```

Version details may differ. A successful result confirms that the container can connect and execute PostGIS functions.

Do not print the connection string: it contains the database password.

### Connect using pgAdmin 4

1. Open pgAdmin 4.
2. Right-click **Servers → Register → Server**.
3. Under **General**, enter a descriptive name. (I just called mine Supabase)
4. Under **Connection**, use the same values as your `.env`:

   | pgAdmin field | Environment variable |
   |---|---|
   | Host name/address | PGHOST |
   | Port | PGPORT |
   | Maintenance database | PGDATABASE |
   | Username | PGUSER |
   | Password | PGPASSWORD |

5. Set **SSL mode** to **Require**, under **SSL** or **Parameters**, depending on your pgAdmin version. (We add SSL to encrypt the data between our computers and supabase since we don't want passwords and stuff to be leaked)
6. Click **Save**.

Enter the original password without surrounding `.env` quotes or URL encoding.

Expand **Databases → postgres**, then open **Query Tool** and run:

```sql
SELECT extensions.postgis_full_version();
```

Returning PostGIS version details confirms the connection works.

### Troubleshooting and extra info

- **Name or service not known:** Check the hostname and DNS resolution inside the container.
- **Network is unreachable with the direct endpoint:** Your environment may lack IPv6 connectivity. Use the session pooler. I've done it this way for us, since i tested IPv6 and it doesn't work for free supabase.
- **Password authentication failed:** Check the database password and the exact username shown for the selected connection method.
- **Free project is paused:** Restore the project from the Supabase dashboard before reconnecting. (This can happen if we haven't connected to the website in a while)
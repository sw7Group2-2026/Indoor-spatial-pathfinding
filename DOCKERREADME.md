# Quick Docker Explanation

Docker **images** are templates containing everything needed to run an application.  
A **container** is a running instance of an image.

Think of it as:

**Image = template/environment**  
**Container = where we actually run it**

`compose.yml` puts multiple Docker services together. For example, our project has a Python environment and a PostGIS database. Compose also lets these services communicate with each other and depend on each other.

## Starting and Stopping

Build and start everything:

```bash
docker compose up --build
```

Run in the background:

```bash
docker compose up --build -d
```

Stop everything:

```bash
docker compose down
```

> `docker compose down -v` also deletes Docker volumes. This means our local database data will be deleted, so only use `-v` when you want to reset the database.

Check the services:

```bash
docker compose ps
```

## Running Python

Run any Python file using our Python container:

```bash
docker compose run --rm py python Folder-Name/filename.py
```

For example:

```bash
docker compose run --rm py python LLM-Testing/main.py
```

`--rm` simply removes the temporary container after the program finishes.

### Python Dependencies

Add required Python libraries to:

```text
Python/requirements.txt
```

They are installed when the Python Docker image is built. If dependencies change, rebuild with:

```bash
docker compose build
```

## PostGIS Database

PostGIS is PostgreSQL with additional support for geographical/spatial data.

Our database exposes:

```yaml
ports:
  - "127.0.0.1:5433:5432"
```

The left side (`5433`) is the port on our computer.  
The right side (`5432`) is PostgreSQL's port inside Docker.

From our computer:

```text
Host: localhost
Port: 5433
```

From another Docker service, such as Python:

```text
Host: postgis-db
Port: 5432
```

Docker Compose automatically creates a network where services can communicate using their service names.

### Connecting with pgAdmin 4

You can use pgAdmin 4 to connect to the PostGIS database running inside Docker.

First, make sure the database is running:

```bash
docker compose up -d
```

You can verify that the container is running and healthy with:

```bash
docker compose ps
```

Then open **pgAdmin 4** and select:

**Servers → Register → Server**

Under the **General** tab, choose any name for the connection, for example:

```text
Name: Local PostGIS
```

Under the **Connection** tab, enter:

```text
Host name/address: 127.0.0.1
Port: 5433
Maintenance database: <POSTGIS_DB>
Username: <POSTGIS_USER>
Password: <POSTGIS_PASSWORD>
```

The values for `POSTGIS_DB`, `POSTGIS_USER`, and `POSTGIS_PASSWORD` are defined in the project's `.env` file.

For example, if `.env` contains:

```env
POSTGIS_DB=mydb
POSTGIS_USER=postgres
POSTGIS_PASSWORD=mypassword
```

the pgAdmin connection would be:

```text
Host name/address: 127.0.0.1
Port: 5433
Maintenance database: mydb
Username: postgres
Password: mypassword
```

> Use port `5433` in pgAdmin because pgAdmin is running on our computer and connects through the Docker port mapping. Services running inside Docker instead connect to `postgis-db:5432`.

After entering the connection details, click **Save**. The PostGIS database should now appear under **Servers** in pgAdmin.

## SQL Files

SQL files placed inside:

```text
Database/sql/
```

are mounted into:

```text
/docker-entrypoint-initdb.d/
```

inside the PostGIS container.

When a **new database is initialized**, Postgres automatically executes these scripts. We can therefore use this folder for things such as creating tables, enabling extensions, or inserting initial data.

For example:

```text
Database/
└── sql/
    ├── 01-enable-postgis.sql
    └── 02-create-tables.sql
```

The actual database data is stored separately in the `postgis_data` Docker volume, allowing us to recreate containers without losing the database.
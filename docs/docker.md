# Running with Docker

[← Back to project README](../README.md)

## Docker

This project runs files in docker. This allows us to run python(or any other file with valid setup for it) without needing to have python downloaded on the computer and prevents us from needing to manually download dependencies (libraries) every time we add something new.

Running this requires Docker Desktop, which you must have started before programming. Please download this before starting.

## Quick Docker Explanation

Docker **images** are templates containing everything needed to run an application.
A **container** is a running instance of an image.

Our `compose.yml` defines the Python service, named `py`. Its image is built
using `app/Dockerfile`.

The Dockerfile uses Python as its entrypoint:

```dockerfile
ENTRYPOINT ["python"]
CMD ["main.py"]
```

This means Python runs automatically. Anything written after `py` in the commands
below is passed to Python. Without arguments, it runs `main.py`.

Run all commands from the project root, where `compose.yml` is located.

## Build and Run

Build the Python image:

```bash
docker compose build
```

Run the application:

```bash
docker compose run --rm py
```

This runs `main.py`. The container exits when the program finishes.

`--rm` removes the temporary container after it exits.

## Running Individual Python Files

Run a file located inside `app/`:

```bash
docker compose run --rm py main.py
```

File paths are relative to `app/`; do not include `app/` in the command.

For files inside packages, use the module path:

```bash
docker compose run --rm py -m device.test
```

Other examples:

```bash
docker compose run --rm py -m database.test
docker compose run --rm py -m interfaces.test
docker compose run --rm py -m interpreter.test
```

## Python Dependencies

Add required third-party libraries to:

```text
app/requirements.txt
```

Dependencies are installed when the image is built. After changing this file,
rebuild:

```bash
docker compose build
```

Check that installed dependencies have compatible requirements:

```bash
docker compose run --rm py -m pip check
```

## Source Code Changes

The Compose configuration mounts the local `app/` folder into the container:

```yaml
volumes:
  - ./app:/usr/src/app
```

Python file changes are available the next time you run a command, without
rebuilding the image.

Changes to `requirements.txt` or the Dockerfile require a rebuild.

## Running with Compose Up

Build and run the application's default command:

```bash
docker compose up --build
```

The container stops once `main.py` finishes. This is expected.

Check service status, including stopped containers:

```bash
docker compose ps -a
```

Remove containers created by `docker compose up`:

```bash
docker compose down
```
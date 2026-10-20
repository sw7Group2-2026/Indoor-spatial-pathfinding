# Python with Docker

Docker provides a shared Python environment so everyone can run the project with the same dependencies.

Run all commands below from the project root (the folder containing `compose.yml`.)

Running docker requires you to have Docker Desktop downloaded. Therefore you must have this downloaded and running before testing-

## Build the Python environment

Ensure docker desktop is running. After, open terminal and run.

```bash
docker compose build py
```

Build once before running code. Rebuild after changing `Python/requirements.txt` or the Dockerfile.

You do not need to rebuild when editing Python files.

## Run Python code

```bash
docker compose run --rm py python Folder-Name/filename.py
```

Paths are relative to the `Python/` directory, which is mounted inside the container. Code edits are available immediately without rebuilding.

Each command creates a container using the built Python image, runs your script, and exits when the script finishes. You do not need to run `docker compose up` first.

### What does --rm do?

`--rm` automatically removes the temporary container after the script finishes, including when it exits with an error.

It does not delete:

- The built Docker image or its installed dependencies.
- Your project files in the mounted `Python/` directory.
- Files your script saves inside that mounted directory.

Files saved elsewhere inside the temporary container are removed with it.

Without `--rm`, the stopped container remains on your computer until you remove it manually.

## Python dependencies

Add dependencies to `Python/requirements.txt`, then rebuild:

```bash
docker compose build py
```

Subsequent runs use the updated image, but you only need to build everytime you update dependencies not the python code.

## Stop the containers

```bash
docker compose down
```

Stops and removes the project's containers and network. Your code and built images are kept.

When using `docker compose run --rm`, the container is removed automatically after the script finishes, so this is usually unnecessary.

## Environment variables

The Python container loads environment variables from the root `.env` file through the `env_file` setting in `compose.yml`.

Keep secrets out of version control. Use `.env.example` to document the required variables without including real credentials.

## Test the Python setup

This test checks that Python runs inside Docker, dependencies are installed, and code changes apply without rebuilding.

Before going through the test, ensure that Docker Desktop is running.

### Test Python and dependencies

Make sure `Python/requirements.txt` includes:

```text
loguru
```

Build the image to install dependencies:

```bash
docker compose build py
```

Run the test:

```bash
docker compose run --rm py python TEST/test.py
```

The output should include:

```text
Python is running successfully inside Docker!
Python version: 3.x.x
```

You should also see Loguru messages containing:

```text
Loguru is working inside Docker!
This is an intentional test warning.
```

The Python version may vary. Loguru adds timestamps and log levels to its messages. The warning is intentional and does not indicate a failure.

### Test code changes without rebuilding

Uncomment this line in `Python/TEST/test.py` and save the file:

```python
print("Code changes are available without rebuilding!", flush=True)
```

Run the test again:

```bash
docker compose run --rm py python TEST/test.py
```

The new message should appear immediately. No rebuild is needed because the `Python/` directory is mounted inside the container.

### Finish testing

When done with testing run `docker compose down` to ensure no containers are still running.
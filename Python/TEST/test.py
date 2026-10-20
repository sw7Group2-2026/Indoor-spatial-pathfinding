# THIS FILE IS FOR TESTING PYTHON CODE RUNNING INSIDE DOCKER AND DEPENDENCIES IN THAT PYTHON CODE

import sys

from loguru import logger

print("Python is running successfully inside Docker!", flush=True)
print(f"Python version: {sys.version.split()[0]}", flush=True)

# Uncomment this line and rerun without rebuilding to test code changes.
# print("Code changes are available without rebuilding!", flush=True)

# These messages confirm that the Loguru dependency is installed.
logger.info("Loguru is working inside Docker!")
logger.warning("This is an intentional test warning.")
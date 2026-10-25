# These are function imports for testing each individual file from each folder
# These are not proper tests, they are simply rudimentary tests i created to see if docker works for now.
from database.test import run as test_database
from device.test import run as test_device
from interfaces.test import run as test_interfaces
from interpreter.test import run as test_interpreter

# This is used for testing library imports
from loguru import logger


test_device()
test_device()
test_interfaces()
test_interpreter()

logger.debug("That's it, beautiful and simple logging!")
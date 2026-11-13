# These are function imports for testing each individual file from each folder
# These are not proper tests, they are simply rudimentary tests i created to see if docker works for now.
from database.test import run as test_database
from device.test import run as test_device
from abstractions.test import run as test_interfaces
from interpreter.test import run as test_interpreter
from database.supa_db_handler import SupaDatabaseHandler
from loguru import logger # type: ignore

# This is used for testing library imports and that packages work
# test_database()
# test_device()
# test_interfaces()
# test_interpreter()
# logger.debug("That's it, beautiful and simple logging!")

# Temporary example of how to use the supaDB handler
sql = None
db = SupaDatabaseHandler()
dbResponse = db.query(sql)
print(dbResponse)

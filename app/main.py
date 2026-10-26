# These are function imports for testing each individual file from each folder
# These are not proper tests, they are simply rudimentary tests i created to see if docker works for now.
from database.test import run as test_database
from device.test import run as test_device
from interfaces.test import run as test_interfaces
from interpreter.test import run as test_interpreter

# This is used for testing library imports
from loguru import logger # type: ignore

from interpreter.llm_api import LLM_API

test_device()
test_device()
test_interfaces()
test_interpreter()

logger.debug("That's it, beautiful and simple logging!")

# Example code that uses llama and allows you to insert query in terminal
ai_model = "llama-3.1-8b-instruct"
system_prompt = "You are a helpful assistant."
ai = LLM_API(ai_model)
query = input("Insert query to ai:\n")
response = ai.prompt(query, system_prompt)
print(response)
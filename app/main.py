from interpreter.llm_api import LLMApi
from database.supa_db_handler import SupaDatabaseHandler
from pathlib import Path

ai = LLMApi("@cf/zai-org/glm-4.7-flash")
db = SupaDatabaseHandler()

prompt_path = (
    Path(__file__).resolve().parent
    / "interpreter"
    / "system_prompt.txt"
)

with open(prompt_path, "r", encoding="utf-8") as file:
    system_prompt = file.read()

question = input("Ask about the building: ")
sql = ai.prompt(question, system_prompt)
dbResponse = db.query(sql)
print(dbResponse)

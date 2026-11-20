from interpreter.glm4flash import GLM4Flash
from interpreter.llama import Llama
from database.supa_db_handler import SupaDatabaseHandler


glmLLLM = GLM4Flash()
llamaLLM = Llama()
db = SupaDatabaseHandler()

question = input("Ask about the building: ")
sql = llamaLLM.prompt(question)
print(sql)
dbResponse = db.query(sql)
print(dbResponse)
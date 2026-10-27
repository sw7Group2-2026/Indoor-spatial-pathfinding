from interpreter.glm4flash import GLM4Flash
from database.supa_db_handler import SupaDatabaseHandler

llm = GLM4Flash()
db = SupaDatabaseHandler()

question = input("Ask about the building: ")
sql = llm.prompt(question)
dbResponse = db.query(sql)
print(dbResponse)

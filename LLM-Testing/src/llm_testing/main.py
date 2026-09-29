from llm_testing.llm_api import LLM_API

# Example code that uses llama and allows you to insert query in terminal
ai_model = "llama-3.1-8b-instruct"
system_prompt = "You are a helpful assistant."
ai = LLM_API(ai_model)
query = input("Insert query to ai:\n")
response = ai.prompt(query, system_prompt)
print(response)

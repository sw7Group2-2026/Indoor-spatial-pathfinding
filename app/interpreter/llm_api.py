import requests
import os
from dotenv import load_dotenv

class LLMApi:
    def __init__(self, ai_model):
        load_dotenv()
        ACCOUNT_ID = os.getenv('ACCOUNT_ID')
        self.API_AUTH_TOKEN = os.getenv('API_AUTH_TOKEN')
        self.cloudflare_workers_api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{ACCOUNT_ID}/ai/run/{ai_model}"
        )

    def prompt(self, prompt, system_setup_prompt):
        response = requests.post(
            self.cloudflare_workers_api_url,
            headers={
                "Authorization": f"Bearer {self.API_AUTH_TOKEN}"
            },
            json={
                "max_tokens": 2048,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": system_setup_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        response_json = response.json()

        result = response_json.get("result", response_json)

        return result["choices"][0]["message"]["content"]
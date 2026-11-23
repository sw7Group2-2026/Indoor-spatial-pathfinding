import requests
from abstractions.cloudflare_llm import CloudflareLLM
from pathlib import Path
from interpreter.user_query import UserQuery

PROMPT_ENGINEERING_INPUT = "prompt_engineering1.txt"
PROMPT_ENGINEERING_VALIDATION = "prompt_engineering2.txt"


class Llama(CloudflareLLM):
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    
    def __init__(self):
            self.input_prompt = self._load_prompt_engineering(PROMPT_ENGINEERING_INPUT)
            self.validation_prompt = self._load_prompt_engineering(PROMPT_ENGINEERING_VALIDATION)
            super().__init__(self.model)

    def _load_prompt_engineering(self, promptFile):
        prompt_path = (
            Path(__file__).resolve().parent.parent
            / promptFile
        )
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def prompt(self, prompt, promptEngineering, responseFormat):
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}",
            headers={
                "Authorization": f"Bearer {self.api_auth_token}",
                "Content-Type": "application/json"
            },
            json={
                "max_tokens": 2048,
                "temperature": 0,
                "messages": [
                    {
                        "role": "system",
                        "content": promptEngineering
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": responseFormat,
                },
            },
            timeout=60
        )

        response_json = response.json()

        if not response_json.get("success", False):
                    raise RuntimeError(f"Cloudflare API error: {response_json}")

        result = response_json["result"]

        return result["response"]
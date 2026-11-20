import requests
from abstractions.cloudflare_llm import CloudflareLLM
from pathlib import Path
from interpreter.user_query import UserQuery


class Llama(CloudflareLLM):
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    
    def __init__(self):
        self.prompt_engineering = self._load_prompt_engineering()
        super().__init__(self.model)

    def _load_prompt_engineering(self):
        prompt_path = (
            Path(__file__).resolve().parent.parent
            / "prompt_engineering.txt"
        )
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()


    def prompt(self, prompt):
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
                        "content": self.prompt_engineering
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "response_format": {
                    "type": "json_schema",
                    "json_schema": UserQuery.getJson(),
                },
            },
            timeout=60
        )

        print("Response:")
        print(response)

        response_json = response.json()

        if not response_json.get("success", False):
                    raise RuntimeError(f"Cloudflare API error: {response_json}")

        print("response.json():")
        print(response_json)

        choices = response_json["result"]["choices"]
        validResponse = UserQuery.validate(choices[0]["message"]["content"])

        print("Valid response:")
        print(validResponse)

        result = response_json["result"]

        return result["response"]
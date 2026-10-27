import requests
from abstractions.cloudflare_llm import CloudflareLLM
from pathlib import Path


class GLM4Flash(CloudflareLLM):
    _model = "@cf/zai-org/glm-4.7-flash"
    
    def __init__(self):
        self.prompt_engineering = self._load_prompt_engineering()
        super().__init__(self._model)

    def _load_prompt_engineering(self):
        prompt_path = (
            Path(__file__).resolve().parent
            / "prompt_engineering.txt"
        )
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    def prompt(self, prompt):
        response = requests.post(
            self.cloudflare_workers_api_url,
            headers={
                "Authorization": f"Bearer {self.api_auth_token}"
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
                ]
            }
        )

        response_json = response.json()

        result = response_json.get("result", response_json)

        return result["choices"][0]["message"]["content"]
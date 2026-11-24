from pathlib import Path

import requests

from abstractions.cloudflare_llm import CloudflareLLM


# The model is used through Cloudflare
class Llama(CloudflareLLM):
    model = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
    
    def __init__(self):
            super().__init__(self.model)

    # Loading the prompt-instructions 
    def _load_prompt_engineering(self, prompt_file):
        prompt_path = (
            Path(__file__).resolve().parent.parent
            / prompt_file
        )
        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read()

    # The user input is sent to Llama with the prompt-instructions and JSON
    def prompt(self, prompt, prompt_engineering, response_format):
        system_prompt = self._load_prompt_engineering(prompt_engineering)
        
        # The request is sent to Coudflare API
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
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                # This make Llama response in the given JSON formate
                "response_format": {
                    "type": "json_schema",
                    "json_schema": response_format,
                }
            },
            timeout=60
        )

        # Converting the respons to JSON
        response_json = response.json()

        # Chrcking if Cloudflare return an error
        if not response_json.get("success", False):
                    raise RuntimeError(f"Cloudflare API error: {response_json}")

        # Get the response from Llama
        result = response_json["result"]

        return result["response"]
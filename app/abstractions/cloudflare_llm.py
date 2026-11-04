from abc import ABC, abstractmethod
from abstractions.llm import LLM
import os
from dotenv import load_dotenv

class CloudflareLLM(LLM):
    model = None

    def __init__(self, ai_model):        
        load_dotenv()
        account_id = os.getenv('ACCOUNT_ID')
        self.api_auth_token = os.getenv('API_AUTH_TOKEN')
        self.cloudflare_workers_api_url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{account_id}/ai/run/{self.model}"
        )
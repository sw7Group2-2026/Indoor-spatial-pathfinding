from abc import ABC, abstractmethod
class LLM(ABC):
    prompt_engineering = None
    
    # Abstract methods are methods which subclasses must implement
    @abstractmethod
    def prompt(self, prompt):
        pass 
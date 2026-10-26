from abc import ABC, abstractmethod

class DB_Handler(ABC):
    @abstractmethod
    def query(self):
        pass
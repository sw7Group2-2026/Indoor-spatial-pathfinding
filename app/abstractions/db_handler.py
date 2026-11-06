from abc import ABC, abstractmethod

class DatabaseHandler(ABC):

    @abstractmethod
    def query(self, sql: str):
        pass
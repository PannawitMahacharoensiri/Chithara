from abc import ABC, abstractmethod

class MusicGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request_data):
        pass

    @abstractmethod
    def check_status(self, task_id):
        pass
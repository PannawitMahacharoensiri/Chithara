import requests
from .base import MusicGeneratorStrategy

class SunoGenerator(MusicGeneratorStrategy):
    def generate(self, request_data):
        response = requests.post(
            "https://api.sunoapi.org/api/v1/generate",
            headers={"Authorization": "Bearer YOUR_TOKEN"},
            json=request_data
        )
        data = response.json()

        return {
            "task_id": data.get("taskId"),
            "status": "PENDING"
        }
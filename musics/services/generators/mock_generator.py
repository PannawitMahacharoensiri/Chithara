import os
import uuid
from django.conf import settings
from .base import MusicGeneratorStrategy

class MockGenerator(MusicGeneratorStrategy):
    def generate(self, request_data):
        # Mimic starting a task
        return {
            "task_id": str(uuid.uuid4()),
            "status": "PENDING",
        }

    def check_status(self, task_id):
        # Mimic completing a task and returning a local URL
        local_audio_url = "/media/test_1234.mp3"
        return {
            "status": "SUCCESS",
            "audio_url": local_audio_url,
        }
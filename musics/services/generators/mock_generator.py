import os
import uuid
from django.conf import settings
from .base import MusicGeneratorStrategy
from musics.enums.generate_state_enum import GenerateState


class MockGenerator(MusicGeneratorStrategy):
    def generate(self, request_data):
        # Mimic starting a task
        return {
            "task_id": str(uuid.uuid4()),
            "status": GenerateState.PENDING,
        }

    def check_status(self, task_id):
        # Mimic completing a task and returning the local file path
        local_audio_path = os.path.join(settings.BASE_DIR, "media", "reference", "test_123.mp3")
        return {
            "status": "SUCCESS",
            "audio_url": local_audio_path,
        }
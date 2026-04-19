from .base import MusicGeneratorStrategy
from musics.enums.generate_state_enum import GenerateState


class MockGenerator(MusicGeneratorStrategy):
    def generate(self, request_data):
        return {
            "audio_url": "/media/mock.mp3",
            "status": GenerateState.COMPLETED,
        }
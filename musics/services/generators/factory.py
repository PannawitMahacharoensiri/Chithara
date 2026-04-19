from django.conf import settings
from .mock_generator import MockGenerator
from .suno_generator import SunoGenerator

def get_generator():
    if settings.GENERATOR_STRATEGY == "mock":
        return MockGenerator()
    return SunoGenerator()
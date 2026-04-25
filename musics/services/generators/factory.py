from django.conf import settings
from .mock_generator import MockGenerator
from .suno_generator import SunoGenerator

def get_generator(strategy=None):
    if not strategy:
        strategy = getattr(settings, "GENERATOR_STRATEGY", "suno")
        
    if strategy == "mock":
        return MockGenerator()
    return SunoGenerator()
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

# VALIDATE: File Type (Expected: mp3)
validate_audio_extension = FileExtensionValidator(
    allowed_extensions=['mp3']
)
def validate_audio_file(value):
    validate_audio_extension(value)

# VALIDATE: File Size maximum 5MB
def validate_file_size(value):
    max_size = 5 * 1024 * 1024
    if value.size > max_size:
        raise ValidationError("File size too large (max 5MB)")
from django import forms
from .models.music_model import Music

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            "display_name",
            "genre",
            "mood",
            "usage_occupation",
            "vocal_preference",
            "generate_description",
        ]
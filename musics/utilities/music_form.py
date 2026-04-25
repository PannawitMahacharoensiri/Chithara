"""
music_form.py:
This file handles data validation and security when users submit data from the frontend (like clicking 'Generate').
Instead of manually checking if every text field is valid, Django Forms automatically verify 
the HTML inputs and securely bind them to the Music database model.
"""
from django import forms
from musics.models.music_model import Music

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = [
            "display_name",
            "genre",
            "mood",
            "usage_occupation",
            "vocal_preference",
            "description",
            "generator_strategy",
        ]
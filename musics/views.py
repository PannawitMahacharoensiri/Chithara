# MusicGenerationController
from django.shortcuts import render
from .services.generators.factory import get_generator
from .models.music_model import Music
from .models.genre_model import Genre
from .models.mood_model import Mood
from musics.enums.generate_state_enum import GenerateState
from django.contrib.auth.decorators import login_required

@login_required
def generate_music(request):
    if request.method == "POST":
        display_name = request.POST.get("display_name")
        genre_id = request.POST.get("genre")
        mood_id = request.POST.get("mood")

        genre = Genre.objects.get(id=genre_id) if genre_id else None
        mood = Mood.objects.get(id=mood_id) if mood_id else None

        request_data = {
            "display_name": display_name,
            "genre": genre.name if genre else None,
            "mood": mood.name if mood else None,
        }

        generator = get_generator()
        result = generator.generate(request_data)

        music = Music.objects.create(
            display_name=display_name,
            genre=genre,
            mood=mood,
            generate_state=result["status"],
            owner=request.user if request.user.is_authenticated else None
        )

        return render(request, "musics/result.html", {"music": music})

    genres = Genre.objects.all()
    moods = Mood.objects.all()

    return render(request, "musics/generate_music.html", {
        "genres": genres,
        "moods": moods
    })
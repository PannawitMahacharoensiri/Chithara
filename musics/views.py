from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse, Http404
from .services.generators.factory import get_generator
from musics.utilities.music_form import MusicForm
from .models.music_model import Music
from musics.enums.generate_state_enum import GenerateState
from django.contrib.auth.decorators import login_required
from musics.utilities.polling_task import start_polling_task
import requests
import re


@login_required
def library_music(request):
    musics = Music.objects.filter(owner=request.user, is_active=True).order_by("-created_at")
    has_pending = musics.filter(generate_state="PENDING").exists()
    return render(request, "musics/library.html", {"musics": musics, "has_pending": has_pending})

def music_detail(request, id):
    music = get_object_or_404(Music, id=id, is_active=True)

    print("STATE:", music.generate_state)
    print("TASK ID:", music.task_id)

    if music.generate_state == "PENDING" and music.task_id:
        generator = get_generator(music.generator_strategy)
        result = generator.check_status(music.task_id)

        print("CHECK RESULT:", result)

        status = result.get("status")

        if status == "SUCCESS":
            music.generate_state = "COMPLETED"

            audio_url = result.get("audio_url")

            if audio_url and not music.audio_url:
                music.audio_url = audio_url

        elif status in ["FAILED", "ERROR"]:
            music.generate_state = "FAILED"

        music.save()

    return render(request, "musics/detail.html", {"music": music})



@login_required
def overview_music(request, id):
    music = get_object_or_404(Music, id=id, owner=request.user, is_active=True)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "generate":
            from django.utils import timezone
            today = timezone.localdate()
            # Count ALL generations (Suno and Mock) for today, including soft-deleted ones
            generation_count = Music.objects.filter(
                owner=request.user,
                created_at__date=today,
            ).exclude(generate_state="DRAFT").exclude(generate_state="CANCELLED").count()
            
            if generation_count >= 20:
                from django.contrib import messages
                messages.error(request, "You have reached your daily limit of 20 generations.")
                return redirect("overview_music", id=music.id)
                    
            generator = get_generator(music.generator_strategy)
            result = generator.generate({
                "display_name": music.display_name,
                "genre": music.genre.name if music.genre else None,
                "mood": music.mood.name if music.mood else None,
                "usage_occupation": music.usage_occupation,
                "vocal_preference": music.vocal_preference,
                "description": music.description,
            })
            
            music.generate_state = result.get("status", "FAILED")
            music.task_id = result.get("task_id")
            music.save()
            
            if music.generate_state == "PENDING":
                start_polling_task(music.id)
                
            return redirect("music_list")
            
        elif action == "cancel":
            music.generate_state = "CANCELLED"
            music.save()
            return redirect("music_list")
            
    return render(request, "musics/overview.html", {"music": music})

# MusicGenerationController
@login_required
def generate_music(request):
    if request.method == "POST":
        form = MusicForm(request.POST)

        if form.is_valid():
            music = form.save(commit=False)
            music.generate_state = "DRAFT"
            music.owner = request.user
            music.save()

            return redirect("overview_music", id=music.id)

    else:
        source_id = request.GET.get('source')
        initial_data = {}
        if source_id:
            try:
                source_music = Music.objects.get(id=source_id, owner=request.user)
                initial_data = {
                    'display_name': f"{source_music.display_name}",
                    'genre': source_music.genre,
                    'mood': source_music.mood,
                    'usage_occupation': source_music.usage_occupation,
                    'vocal_preference': source_music.vocal_preference,
                    'description': source_music.description,
                    'generator_strategy': source_music.generator_strategy,
                }
            except Music.DoesNotExist:
                pass
        form = MusicForm(initial=initial_data)

    return render(request, "musics/generate_music.html", {"form": form})

def check_music_status(request, id):
    music = get_object_or_404(Music, id=id)

    # only check if still pending
    if music.generate_state == "PENDING" and music.task_id:
        generator = get_generator(music.generator_strategy)
        result = generator.check_status(music.task_id)

        status = result.get("status")

        if status == "SUCCESS":
            music.generate_state = "COMPLETED"

            # depends on API response
            audio_url = result.get("audio_url")

            if audio_url:
                music.audio_url = audio_url

        elif status in ["FAILED", "ERROR"]:
            music.generate_state = "FAILED"

        music.save()

    return redirect("music_detail", id=music.id)

@login_required
def cancel_music(request, id):
    music = get_object_or_404(Music, id=id, owner=request.user)
    if request.method == "POST":
        if music.generate_state == "PENDING":
            music.generate_state = "CANCELLED"
            music.save()
            # Alternatively, we could delete it: music.delete()
            # But setting it to CANCELLED stops the poller and keeps the record for reference
    return redirect("music_list")

@login_required
def delete_music(request, id):
    music = get_object_or_404(Music, id=id, owner=request.user)
    if request.method == "POST":
        music.is_active = False
        music.save()
        return redirect("music_list")
    return render(request, "musics/confirm_delete.html", {"music": music})


@login_required
def download_music(request, id):
    """
    Proxy view to download music files.
    This ensures the 'download' attribute works even for cross-origin URLs (like Suno CDN).
    """
    music = get_object_or_404(Music, id=id, owner=request.user)
    if not music.audio_url:
        raise Http404("Audio URL not found for this track.")

    url = music.audio_url

    # Handle relative local URLs (e.g., /media/song.mp3)
    if url.startswith('/'):
        url = request.build_absolute_uri(url)

    try:
        # Fetch the file from the remote source
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()

        # Prepare the streaming response
        def file_iterator(chunk_size=8192):
            for chunk in response.iter_content(chunk_size=chunk_size):
                yield chunk

        # Set appropriate content type from source or fallback to audio/mpeg
        content_type = response.headers.get('Content-Type', 'audio/mpeg')

        # Create StreamingHttpResponse for better performance with audio files
        django_response = StreamingHttpResponse(file_iterator(), content_type=content_type)

        # Format a clean filename for the user
        safe_name = re.sub(r'[^\w\s\.-]', '', music.display_name)
        if not safe_name: safe_name = "track"
        filename = f"{safe_name}.mp3"

        # Force download with Content-Disposition
        django_response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return django_response

    except requests.exceptions.RequestException as e:
        # If the external URL fails, we could log it or show an error
        return HttpResponse(f"Failed to fetch audio from source: {str(e)}", status=502)
    except Exception as e:
        return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)
from django.shortcuts import render, get_object_or_404, redirect
from .services.generators.factory import get_generator
from .forms import MusicForm
from .models.music_model import Music
from musics.enums.generate_state_enum import GenerateState
from django.contrib.auth.decorators import login_required
import requests
from django.core.files.base import ContentFile


@login_required
def library_music(request):
    musics = Music.objects.filter(owner=request.user).order_by("-created_at")
    return render(request, "musics/list.html", {"musics": musics})

def music_detail(request, id):
    music = get_object_or_404(Music, id=id)

    print("STATE:", music.generate_state)
    print("TASK ID:", music.task_id)

    if music.generate_state == "PENDING" and music.task_id:
        generator = get_generator()
        result = generator.check_status(music.task_id)

        print("CHECK RESULT:", result)

        status = result.get("status")

        if status == "SUCCESS":
            music.generate_state = "COMPLETED"

            audio_url = result.get("audio_url")

            if audio_url and not music.audio_file:
                if audio_url.startswith("http://") or audio_url.startswith("https://"):
                    audio_response = requests.get(audio_url)
                    if audio_response.status_code == 200:
                        music.audio_file.save(
                            f"music_{music.id}.mp3",
                            ContentFile(audio_response.content),
                            save=False
                        )
                else:
                    import os
                    if os.path.exists(audio_url):
                        with open(audio_url, "rb") as f:
                            music.audio_file.save(
                                f"music_{music.id}.mp3",
                                ContentFile(f.read()),
                                save=False
                            )

        elif status in ["FAILED", "ERROR"]:
            music.generate_state = "FAILED"

        music.save()

    return render(request, "musics/detail.html", {"music": music})

import threading
import time
from django.db import connection

def poll_suno_status(music_id):
    try:
        from musics.models.music_model import Music
        from musics.services.generators.factory import get_generator
        from django.core.files.base import ContentFile
        import requests
        
        time.sleep(2) # Give DB a moment
        music = Music.objects.get(id=music_id)
        generator = get_generator()
        
        for _ in range(60): # 10 minutes maximum
            time.sleep(10)
            music.refresh_from_db()
            
            if music.generate_state != "PENDING":
                break
                
            result = generator.check_status(music.task_id)
            status = result.get("status")
            
            if status == "SUCCESS":
                music.generate_state = "COMPLETED"
                audio_url = result.get("audio_url")
                if audio_url and not music.audio_file:
                    if audio_url.startswith("http://") or audio_url.startswith("https://"):
                        audio_response = requests.get(audio_url)
                        if audio_response.status_code == 200:
                            music.audio_file.save(
                                f"music_{music.id}.mp3",
                                ContentFile(audio_response.content),
                                save=False
                            )
                    else:
                        import os
                        if os.path.exists(audio_url):
                            with open(audio_url, "rb") as f:
                                music.audio_file.save(
                                    f"music_{music.id}.mp3",
                                    ContentFile(f.read()),
                                    save=False
                                )
                music.save()
                break
            elif status in ["FAILED", "ERROR"]:
                music.generate_state = "FAILED"
                music.save()
                break
    except Exception as e:
        print(f"Background poll failed: {e}")
    finally:
        connection.close()

@login_required
def overview_music(request, id):
    music = get_object_or_404(Music, id=id, owner=request.user)
    
    if request.method == "POST":
        action = request.POST.get("action")
        
        if action == "generate":
            generator = get_generator()
            result = generator.generate({
                "display_name": music.display_name,
                "genre": music.genre.name if music.genre else None,
                "mood": music.mood.name if music.mood else None,
                "usage_occupation": music.usage_occupation,
                "vocal_preference": music.vocal_preference,
                "generate_description": music.generate_description,
            })
            
            music.generate_state = result.get("status", "FAILED")
            music.task_id = result.get("task_id")
            music.save()
            
            if music.generate_state == "PENDING":
                thread = threading.Thread(target=poll_suno_status, args=(music.id,))
                thread.daemon = True
                thread.start()
                
            return redirect("music_list")
            
        elif action == "cancel":
            music.delete()
            return redirect("generate_music")
            
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
        form = MusicForm()

    return render(request, "musics/generate_music.html", {"form": form})

def check_music_status(request, id):
    music = get_object_or_404(Music, id=id)

    # only check if still pending
    if music.generate_state == "PENDING" and music.task_id:
        generator = get_generator()
        result = generator.check_status(music.task_id)

        status = result.get("status")

        if status == "SUCCESS":
            music.generate_state = "COMPLETED"

            # ⚠️ depends on API response
            audio_url = result.get("audio_url")

            if audio_url:
                music.audio_file = audio_url  # temporary (we improve later)

        elif status in ["FAILED", "ERROR"]:
            music.generate_state = "FAILED"

        music.save()

    return redirect("music_detail", id=music.id)

@login_required
def cancel_music(request, id):
    music = get_object_or_404(Music, id=id, owner=request.user)
    if request.method == "POST":
        if music.generate_state == "PENDING":
            music.generate_state = "FAILED"
            music.save()
            # Alternatively, we could delete it: music.delete()
            # But setting it to FAILED stops the poller and keeps the record for reference
    return redirect("music_list")
"""
polling_task.py:
This file contains operations that run independently in the background (like polling the Suno API).
By putting this logic in a background 'thread', the website can instantly respond to the user 
(e.g., redirecting them to the library) while the server silently continues checking the generation status.
"""
import threading
import time
from django.db import connection

def _poll_suno_status(music_id):
    try:
        from musics.models.music_model import Music
        from musics.services.generators.factory import get_generator
        
        time.sleep(2) # Give DB a moment
        music = Music.objects.get(id=music_id)
        generator = get_generator(music.generator_strategy)
        
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
                if audio_url and not music.audio_url:
                    music.audio_url = audio_url
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

def start_polling_task(music_id):
    """Starts the background polling task for music generation."""
    thread = threading.Thread(target=_poll_suno_status, args=(music_id,))
    thread.daemon = True
    thread.start()

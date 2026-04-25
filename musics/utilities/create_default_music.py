"""
create_default_music.py:
This file contains Django signals which act as automated event triggers.
For example, the signal below automatically runs immediately after a new user creates an account,
seamlessly inserting the default 'WIN' theme song into their library without them having to do anything.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timezone
from musics.models.music_model import Music

@receiver(post_save, sender="accounts.User")
def create_default_music_for_new_user(sender, instance, created, **kwargs):
    if created:
        from musics.models.genre_model import Genre
        from musics.models.mood_model import Mood
        
        genre, _ = Genre.objects.get_or_create(name="Jazz")
        mood, _ = Mood.objects.get_or_create(name="Excited")
        
        music = Music.objects.create(
            owner=instance,
            display_name="WIN",
            task_id="1032ba4f9b417a4bbba5cdddfdd534f1",
            genre=genre,
            mood=mood,
            generate_state="COMPLETED",
            generator_strategy="suno",
            audio_url="/media/WIN.mp3",
            usage_occupation="Theme Song",
            vocal_preference="Any",
            description="The official Chithara theme song."
        )
        
        target_date = datetime(2026, 4, 20, 10, 6, tzinfo=timezone.utc)
        Music.objects.filter(id=music.id).update(created_at=target_date)

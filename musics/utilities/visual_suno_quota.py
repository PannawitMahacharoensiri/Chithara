"""
visual_suno_quota.py:
A 'context processor' is a Django feature that automatically injects data into EVERY HTML template across your site.

This specific file calculates the user's daily music generation quota (Suno/Mock limits).
Because it's a context processor, variables like 'suno_remaining' are automatically available 
in the navbar (base.html) without needing to pass them manually from every single view.
"""
from django.utils import timezone
from musics.models.music_model import Music

def suno_quota(request):
    if not request.user.is_authenticated:
        return {}
        
    today = timezone.localdate()
    
    # Count ALL generations (Suno and Mock) for today, including soft-deleted ones
    used_count = Music.objects.filter(
        owner=request.user,
        created_at__date=today,
    ).exclude(generate_state="DRAFT").exclude(generate_state="CANCELLED").count()
    
    daily_limit = 20
    remaining = max(0, daily_limit - used_count)
    
    return {
        "suno_daily_limit": daily_limit,
        "suno_used": used_count,
        "suno_remaining": remaining,
    }

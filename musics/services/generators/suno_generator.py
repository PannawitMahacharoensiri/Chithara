import requests
from .base import MusicGeneratorStrategy
from django.conf import settings


class SunoGenerator(MusicGeneratorStrategy):

    def generate(self, request_data):

        prompt_parts = []

        if request_data.get("genre"):
            prompt_parts.append(f"a {request_data.get('genre')} song")

        if request_data.get("mood"):
            prompt_parts.append(f"with a {request_data.get('mood')} mood")

        if request_data.get("usage_occupation"):
            prompt_parts.append(f"suitable for {request_data.get('usage_occupation')}")

        if request_data.get("vocal_preference"):
            prompt_parts.append(f"with {request_data.get('vocal_preference')} vocals")

        if request_data.get("description"):
            prompt_parts.append(request_data.get("description"))

        prompt = " ".join(prompt_parts)

        if not prompt:
            prompt = "A simple music track"

        prompt = " ".join(prompt.split())

        instrumental = not request_data.get("vocal_preference")

        payload = {
            "prompt": prompt,
            "customMode": False,
            "model": "V4_5",
            "instrumental": instrumental,
            "callBackUrl": "http://localhost:8000/",
        }

        response = requests.post(
            "https://api.sunoapi.org/api/v1/generate",
            json=payload,
            headers={
                "Authorization": f"Bearer {settings.SUNO_API_KEY}",
                "Content-Type": "application/json"
            }
        )

        print("STATUS CODE:", response.status_code)
        print("RESPONSE TEXT:", response.text)

        if not response.ok:
            return {"task_id": None, "status": "FAILED"}

        data = response.json() or {}

        print("RESPONSE:", data)

        if data.get("code") != 200:
            return {"task_id": None, "status": "FAILED"}

        inner = data.get("data") or {}

        task_id = inner.get("taskId")

        return {
            "task_id": task_id,
            "status": "PENDING"
        }

    def check_status(self, task_id):
        response = requests.get(
            "https://api.sunoapi.org/api/v1/generate/record-info",
            headers={
                "Authorization": f"Bearer {settings.SUNO_API_KEY}"
            },
            params={"taskId": task_id}
        )

        if not response.ok:
            return {"status": "FAILED"}

        data = response.json() or {}
        print("STATUS RESPONSE:", data)

        result = data.get("data") or {}

        audio_url = None

        response_data = result.get("response") or {}
        suno_data = response_data.get("sunoData") or []

        if suno_data:
            first = suno_data[0]
            audio_url = first.get("sourceAudioUrl") or first.get("audioUrl")

        if not audio_url:
            clips = result.get("clips") or []
            if clips:
                audio_url = clips[0].get("audioUrl")

        return {
            "status": result.get("status"),
            "audio_url": audio_url
        }
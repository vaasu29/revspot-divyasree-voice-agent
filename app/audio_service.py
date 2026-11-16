import os
import asyncio
import edge_tts
import io

TEMP_CACHE_DIR = os.path.join("app", "static", "cache")
os.makedirs(TEMP_CACHE_DIR, exist_ok=True)

class AudioService:
    @staticmethod
    async def synthesize_to_bytes(text: str, voice: str = "en-IN-PrabhatNeural") -> bytes:
        """
        Synthesizes text to MP3 bytes using Edge-TTS for low-latency live streaming.
        """
        # Auto-switch to Hindi voice if text contains Hindi characters or keywords
        if any(w in text.lower() for w in ["sir ji", "aapka", "dhanyawad", "shukriya", "bilkul", "waqt"]):
            voice = "hi-IN-SwaraNeural"

        communicate = edge_tts.Communicate(text, voice)
        mp3_buffer = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                mp3_buffer.write(chunk["data"])
        return mp3_buffer.getvalue()

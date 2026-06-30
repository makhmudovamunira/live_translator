from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from another_fastapi_jwt_auth import AuthJWT
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

translate_router = APIRouter(
    prefix="/translate",
    tags=["Translation"]
)

recognizer = sr.Recognizer()


@translate_router.get("/")
def translate(text: str):
    print(text)
    translated_text = GoogleTranslator(
        source="uz",
        target="en"
    ).translate(text)
    print(translated_text)

    tts = gTTS(text=translated_text, lang="en")
    tts.save("output.mp3")

    return {
        "success": True,
        "translation": translated_text,
        "audio_url": "http://127.0.0.1:8000/translate/audio"
    }

from fastapi.responses import FileResponse
import os

@translate_router.get("/audio")
async def get_audio():
    if os.path.exists("output.mp3"):
        return FileResponse("output.mp3", media_type="audio/mpeg")
    raise HTTPException(status_code=404, detail="Audio topilmadi")
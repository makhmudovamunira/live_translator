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


@translate_router.post("/voice1", status_code=status.HTTP_200_OK)
async def translate_voice(
        file: UploadFile = File(...),
        Authorize: AuthJWT = Depends()
):
    # try:
    #     # JWT Token borligini va to'g'riligini tekshirish
    #     Authorize.jwt_required()
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Ruxsat berilmagan! Avval tizimga kiring."
    #     )

    # Kelgan audio faylni o'qish
    audio_bytes = await file.read()

    try:
        # Audioni SpeechRecognition formati bo'yicha yuklaymiz
        audio_data = sr.AudioData(audio_bytes, sample_rate=16000, sample_width=2)

        # 1. Ovozni o'zbekcha matnga aylantirish
        text = recognizer.recognize_google(audio_data, language="uz-UZ")

        if not text:
            raise HTTPException(status_code=400, detail="Ovozda hech qanday so'z aniqlanmadi.")

        # 2. Matnni ingliz tiliga tarjima qilish
        translated = GoogleTranslator(source='uz', target='en').translate(text)

        return {
            "status": "success",
            "original_text": text,
            "translated_text": translated
        }

    except sr.UnknownValueError:
        raise HTTPException(
            status_code=400,
            detail="Ovoz formati mos kelmadi yoki tushunarsiz. Aniqroq gapirib ko'ring."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Xatolik: {str(e)}")

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
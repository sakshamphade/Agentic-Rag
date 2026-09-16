import io
import os
import traceback
import pprint

import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import which

# ====================================================
# FFMPEG CONFIGURATION
# ====================================================

FFMPEG = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg\bin\ffmpeg.exe"
FFPROBE = r"C:\ffmpeg-8.1.2-essentials_build\ffmpeg\bin\ffprobe.exe"

# Tell pydub exactly where ffmpeg is
AudioSegment.converter = FFMPEG

# Add ffmpeg folder to PATH so pydub can find ffprobe
ffmpeg_folder = os.path.dirname(FFMPEG)
os.environ["PATH"] = ffmpeg_folder + os.pathsep + os.environ["PATH"]

print("=" * 60)
print("FFmpeg Exists :", os.path.exists(FFMPEG))
print("FFprobe Exists:", os.path.exists(FFPROBE))
print("which(ffmpeg) :", which("ffmpeg"))
print("which(ffprobe):", which("ffprobe"))
print("=" * 60)


class SpeechToText:

    @staticmethod
    def convert(audio):

        try:

            print("\n========== AUDIO OBJECT ==========")
            pprint.pprint(audio)
            print("==================================\n")

            recognizer = sr.Recognizer()

            # -------------------------------------------------
            # Audio bytes
            # -------------------------------------------------
            audio_bytes = io.BytesIO(audio["bytes"])

            print("Step 1 : Bytes Loaded")

            # -------------------------------------------------
            # Convert WEBM -> WAV
            # -------------------------------------------------
            sound = AudioSegment.from_file(
                audio_bytes,
                format=audio.get("format", "webm")
            )

            print("Step 2 : WEBM Loaded")

            wav_buffer = io.BytesIO()

            sound.export(
                wav_buffer,
                format="wav"
            )

            print("Step 3 : WAV Created")

            wav_buffer.seek(0)

            # -------------------------------------------------
            # Read WAV
            # -------------------------------------------------
            with sr.AudioFile(wav_buffer) as source:
                audio_data = recognizer.record(source)

            print("Step 4 : Audio Read")

            # -------------------------------------------------
            # Speech Recognition
            # -------------------------------------------------
            text = recognizer.recognize_google(audio_data)

            print("Step 5 : Recognition Done")

            return True, text

        except Exception as e:
            print(traceback.format_exc())
            return False, traceback.format_exc()
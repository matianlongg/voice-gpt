import io
import traceback
import wave
from src.asr.base import ASR
import threading
import time
from openai import OpenAI
from pydub import AudioSegment

def audio_frame_to_wav_bytes(audio_frame):
    with wave.open("temp.wav", 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(16000)
        wav_file.writeframes(b''.join(audio_frame))

class OpenAIASR(ASR):
    def __init__(self, 
            model='whisper-1',
            sample_rate=16000,
            callback=None,
            api_key=None,
            base_url=None,
            **kwargs) -> None:
        super().__init__()
        self.callback = callback
        self.model = model
        self.sample_rate = sample_rate
        self.audio_frames = []
        self.cache_audio_frames = []
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def start(self, is_playing):
        super().start(is_playing)
        self.cache_audio_frames = []
        self.audio_frames = []
        print('Recognition started')

    def stop(self):
        super().stop()
        self._process_audio()

        print('Recognition stopped')

    def send_audio_frame(self, frame):
        super().send_audio_frame(frame)
        self.audio_frames.append(frame)

    def _process_audio(self):
        if not self.audio_frames:
            return
        audio_frame_to_wav_bytes(self.audio_frames)
        try:
            with open("temp.wav", "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file ,
                    response_format="text"
                )
            self.callback(transcription, self.is_playing)
        except Exception as e:
            traceback.print_exc()
        self.audio_frames = []
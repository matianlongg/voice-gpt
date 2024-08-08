import importlib
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

import sys
import time
from config import config
from src.audio_input.pcm_recorder import Recorder
from src.audio_player.pcm_player import PcmPlayer
from src.llm.aliyun_llm import AliyunLLM
from src.tts.aliyun_tts import AliyunTTS
from src.asr.aliyun_recognizer import AliyunRecognizer
import dashscope

# 阿里云key
# https://ai.aliyun.com/nls/trans
if 'DASHSCOPE_API_KEY' in os.environ:
    dashscope.api_key = os.environ['DASHSCOPE_API_KEY']

class MainApp:
    def __init__(self):
        self.audio_input = Recorder(self.audio_callback)
        self.recognition = None
        self.llm = AliyunLLM()
        self.audio_player = PcmPlayer(self.on_play_end)
        self.speech_synthesizer = None
        self._audio_frame_count = 0
        self._speech_start_time = None
        self._last_speech_time = None
        self._is_playing = False
        self._cache_text = ""

    def audio_callback(self, indata, frames, audio_time, status, voice_detected):
        """Send audio data to the recognition service"""
        current_time = time.time()
        self.handle_voice_detection(voice_detected, current_time)
        if self.recognition is not None and self.audio_input.is_working():
            self._audio_frame_count += 1
            buffer = indata.tobytes()
            sys.stdout.write("\rRecording: [{:<10}]".format('=' * self._audio_frame_count))
            sys.stdout.flush()
            self.recognition.send_audio_frame(buffer)

    def handle_voice_detection(self, voice_detected, current_time):
        if voice_detected:
            self.start_voice_recognition(current_time)
        else:
            self.stop_voice_recognition_if_necessary(current_time)

    def start_voice_recognition(self, current_time):
        if self._speech_start_time is None:
            self._speech_start_time = current_time
        self._last_speech_time = current_time
        if self.recognition is None:
            self.start_recognition()
            print("\nRecognition init and started")

    def stop_voice_recognition_if_necessary(self, current_time):
        if self._last_speech_time and current_time - self._last_speech_time > 3.0:
            if self.recognition is not None:
                self.stop_recognition()
                print("\nRecognition stopped")
            self._speech_start_time = None
            self._last_speech_time = None

    def start_recognition(self):
        if self.speech_synthesizer is None:
            self.speech_synthesizer = AliyunTTS(self.audio_player)
        self.recognition = AliyunRecognizer(callback=self.chat)
        self.recognition.start()
        self._audio_frame_count = 0

    def stop_recognition(self):
        try:
            self.recognition.stop()
            self.recognition = None
            print("recognition已关闭")
        except Exception as e :
            print(f"Error stopping recognition: {e}")


    def speech_synthesizer_callback(self, audio_data):
        self.audio_player.play(audio_data)

    def start(self):
        self.audio_input.start()

    def stop(self):
        self.audio_input.stop()
        self.stop_recognition()
        
    def chat(self, text):
        if self._is_playing:
            self._cache_text += text
            return
        self._is_playing = True
        answer = ""
        for text in self.llm(text):
            answer += text
            self.speech_synthesizer.call_synthesizer(text)
        print(answer)
        self.speech_synthesizer.streaming_complete()
        
    def on_play_end(self):
        print("on_play_end")
        if self.speech_synthesizer:
            print("interrupt playing tts")
            self.speech_synthesizer.interrupt()
            self.speech_synthesizer = None
        self._is_playing = False     
        print("缓冲内容", self._cache_text)   
        self._cache_text = ""

if __name__ == "__main__":
    app = MainApp()
    app.start()
    try:
        while True:
            time.sleep(0.1)  # 保持主线程运行
    except KeyboardInterrupt:
        app.stop()
        print("\nProgram terminated by user.")

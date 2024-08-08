from src.tts.base import ITTS
import queue
import sys
import threading
from src.audio_player.base import IAudioPlayer
from dashscope.audio.tts_v2 import ResultCallback, SpeechSynthesizer, AudioFormat


class Callback(ResultCallback):
    def __init__(self, player: IAudioPlayer):
        self.player = player
        self._synth_frame_count = 0

    def on_open(self):
        print('websocket is open.')
        self._synth_frame_count = 0

    def on_complete(self):
        print('\nspeech synthesis task complete successfully.')

    def on_error(self, message):
        print(f'speech synthesis task failed, {message}')

    def on_close(self):
        print('websocket is closed.')

    def on_event(self, message):
        self._synth_frame_count += 1
        sys.stdout.write("\rPlaying: [{:<10}]".format('=' * self._synth_frame_count))
        sys.stdout.flush()

    def on_data(self, data: bytes) -> None:
        # save audio to file
        self.player.play(data)

class AliyunTTS(ITTS):
    
    def __init__(self, player: IAudioPlayer):
        self.synthesizer = None  # 初始化阿里云的语音合成对象
        self.message_queue = queue.Queue()
        self._player = player
        self.synthesizer_callback = Callback(self._player)
        consumer_thread = threading.Thread(target=self.consumer, args=())
        consumer_thread.start()

    def synthesize(self, text):
        print(f"Synthesizing speech with Aliyun: {text}")
        # 实现具体的语音合成逻辑
        self.synthesizer.call_synthesizer(text)

    def interrupt(self):
        print("Interrupting Aliyun synthesizer")
        # 实现具体的打断逻辑
        self._player.cancel_play()
        
    def consumer(self):
        # Call the speech synthesizer callback
        self.create_synthesizer()
        while True:
            message = self.message_queue.get()
            if message == "complete":
                self.synthesizer.streaming_complete()
                # notify tts player audio complete
                self.streaming_complete()
                self._player.feed_finish()
                break
            else:
                print("streaming synthesizer call with text: ", message)
                self.synthesizer.streaming_call(message)
                self.message_queue.task_done()  # 表示任务已完成

    def create_synthesizer(self):
        self.synthesizer = SpeechSynthesizer(
            model='cosyvoice-v1',
            voice='longxiaochun',
            format=AudioFormat.PCM_24000HZ_MONO_16BIT,
            callback=self.synthesizer_callback)
        # start player
        print("start player")
        self._player.start_play()

    def call_synthesizer(self, text: str):
        self.message_queue.put_nowait(text)
        
    def streaming_complete(self):
        self.message_queue.put_nowait("complete")
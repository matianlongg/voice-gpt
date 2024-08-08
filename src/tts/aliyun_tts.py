from src.tts.base import TTS
import queue
import sys
import threading
from src.audio_output.base import AudioOutput 
from dashscope.audio.tts_v2 import ResultCallback, SpeechSynthesizer, AudioFormat

class Callback(ResultCallback):
    """
    用于处理语音合成结果的回调类。

    方法:
        on_open(): 在 WebSocket 打开时调用。
        on_complete(): 在语音合成任务成功完成时调用。
        on_error(message): 在语音合成任务失败时调用。
        on_close(): 在 WebSocket 关闭时调用。
        on_event(message): 在收到事件消息时调用。
        on_data(data): 在收到音频数据时调用。
    """
    def __init__(self, player: AudioOutput):
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
        self.player.play(data)

class AliyunTTS(TTS):
    """
    阿里云语音合成类，实现了 TTS 抽象基类。

    属性:
        synthesizer (SpeechSynthesizer): 阿里云语音合成器对象。
        message_queue (Queue): 用于存储待合成文本的队列。
        _player (AudioPlayer): 用于播放合成语音的音频播放器。
        synthesizer_callback (Callback): 用于处理语音合成结果的回调对象。

    方法:
        __init__(player): 初始化阿里云语音合成类。
        synthesize(text): 合成给定的文本为语音。
        interrupt(): 打断当前的语音合成。
        consumer(): 消费消息队列并调用语音合成器。
        create_synthesizer(): 创建并配置语音合成器对象。
        call_synthesizer(text): 将文本放入消息队列以进行语音合成。
        streaming_complete(): 通知语音合成流已完成。
    """
    def __init__(self, player: AudioOutput):
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
        # 创建语音合成器
        self.create_synthesizer()
        while True:
            message = self.message_queue.get()
            if message == "complete":
                self.synthesizer.streaming_complete()
                # 通知 TTS 播放器音频已完成
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
        # 启动播放器
        print("start player")
        self._player.start_play()

    def call_synthesizer(self, text: str):
        self.message_queue.put_nowait(text)
        
    def streaming_complete(self):
        self.message_queue.put_nowait("complete")

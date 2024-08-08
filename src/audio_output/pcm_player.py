from src.audio_output.base import AudioOutput
import threading
import time
import pyaudio

class PlayerCallback:
    """
    用于在播放完成后执行特定操作的回调接口。

    方法:
        on_play_end(): 播放结束时调用的方法。
    """

    def __init__(self, play_end_callback) -> None:
        """
        初始化回调对象。

        参数:
            play_end_callback (function): 播放结束后调用的回调函数。
        """
        self.play_end_callback = play_end_callback

    def on_play_end(self):
        """播放结束时调用。默认实现不执行任何操作，子类可以重写此方法提供具体行为。"""
        self.play_end_callback()


class PcmPlayer(AudioOutput):
    """
    PCM 音频播放器类，负责在单独的线程中播放 PCM 格式的音频数据。

    属性:
        callback (PlayerCallback): 播放完成后调用的回调对象，默认为 None。
        player (PyAudio): 管理音频设备的 PyAudio 实例。
        stream (Stream): 用于播放音频数据的音频流实例。
        play_thread (Thread): 用于异步音频播放的线程实例。
        frame_data_queue (list): 存放待播放音频帧的队列。
        _is_end (bool): 指示是否停止播放的标志。

    方法:
        __init__(play_end_callback=None): 初始化播放器并设置回调对象。
        start_play(): 开始音频播放。
        _play_in_thread(): 在独立线程中播放音频数据的内部方法。
        play(frame_data): 添加音频帧到播放队列。
        stop_play(): 停止音频播放并在播放后调用回调函数。
        cancel_play(): 清空播放队列并立即停止播放。
        __del__(): 确保资源正确释放的析构函数。
    """

    def __init__(self, play_end_callback=None):
        """
        初始化 PcmPlayer 实例，创建 PyAudio 和音频流实例，并准备播放线程。

        参数:
            play_end_callback (function): 可选参数，指定播放结束后的回调函数。
        """
        self.callback = PlayerCallback(play_end_callback)
        self.player = pyaudio.PyAudio()
        self.stream = self.player.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=24000,
            output=True
        )
        self.play_thread = None
        self.frame_data_queue = []
        self._is_end = False

    def start_play(self):
        """开始音频播放，启动播放线程。"""
        self._is_end = False
        self.stream.start_stream()
        self.play_thread = threading.Thread(target=self._play_in_thread)
        self.play_thread.start()

    def _play_in_thread(self):
        """在独立线程中循环播放音频数据，直到队列为空或标记停止。"""
        while self.frame_data_queue or not self._is_end:
            if not self.frame_data_queue:
                time.sleep(0.1)
                continue
            frame_data = self.frame_data_queue.pop(0)
            self.stream.write(frame_data)

        if self._is_end:
            self.stream.stop_stream()
            self.callback.on_play_end()

    def play(self, frame_data):
        """
        将音频帧加入播放队列。

        参数:
            frame_data (bytes): 单帧 PCM 音频数据。
        """
        self.frame_data_queue.append(frame_data)

    def feed_finish(self):
        """设置结束标志，导致播放线程退出循环，从而停止播放。"""
        self._is_end = True

    def cancel_play(self):
        """清空播放队列并立即停止播放。"""
        self.frame_data_queue.clear()
        self._is_end = True

    def __del__(self):
        """确保在 PcmPlayer 对象删除时关闭音频流和 PyAudio 实例。"""
        self.stream.close()
        self.player.terminate()

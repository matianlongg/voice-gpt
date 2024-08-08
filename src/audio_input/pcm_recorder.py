import numpy as np
import sounddevice as sd
from src.audio_input.base import AudioInput

# 录音配置参数
SAMPLE_RATE = 16000  # 采样率（赫兹）
CHANNELS = 1  # 单声道
DTYPE = 'int16'  # 音频样本的数据类型
FORMAT_PCM = 'pcm'  # 音频数据格式
BLOCK_SIZE = 1280  # 每缓冲区的帧数，相当于16kHz时约80毫秒
ENERGY_THRESHOLD = 2  # 能量阈值

class Recorder(AudioInput):
    """
    使用 sounddevice 库管理 PCM 音频录音的类。

    属性:
        _is_working (bool): 指示录音机当前是否处于活动状态。
        stream (sd.InputStream): 用于录音的 InputStream 类的实例。

    方法:
        start(): 开始录音过程。
        stop(): 停止录音过程。
        is_working(): 返回录音机的当前状态。
        __del__(): 在对象删除时通过关闭音频流确保适当的清理。
    """

    def __init__(self, callback):
        """
        使用指定的录音参数和回调函数初始化 Recorder。

        参数:
            callback (function): 用户定义的处理传入音频数据的函数。
        """
        self._is_working = False
        self.user_callback = callback
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype=DTYPE,
            blocksize=BLOCK_SIZE,
            callback=self._internal_callback
        )

    def _internal_callback(self, indata, frames, time, status):
        """内部回调函数，用于检测语音活动并调用用户回调。"""
        if status:
            print(status)
        
        # 计算音频信号的能量
        energy = np.linalg.norm(indata) / frames
        # 检查能量是否超过阈值
        voice_detected = energy > ENERGY_THRESHOLD
        # 检测到语音活动，调用用户回调
        self.user_callback(indata, frames, time, status, voice_detected)

    def start(self):
        """开始录音过程。"""
        self.stream.start()
        self._is_working = True

    def stop(self):
        """停止录音过程。"""
        self._is_working = False
        self.stream.stop()

    def is_working(self):
        """
        检查录音机当前是否处于活动状态。

        返回:
            bool: 如果正在录音，则返回 True，否则返回 False。
        """
        return self._is_working

    def __del__(self):
        """确保在 Recorder 对象删除时关闭音频流。"""
        self.stream.close()

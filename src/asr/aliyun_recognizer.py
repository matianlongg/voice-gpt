
from src.asr.base import IRecognition
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

class MyRecognitionCallback(RecognitionCallback):
    def __init__(self, callback):
        super().__init__()
        self._player_callback = None
        self._audio_player = None
        self._callback = callback
        self._audio_player = None

    def on_open(self) -> None:
        print('Recognition open')  # recognition open

    def on_complete(self) -> None:
        print('Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)
        # Forcefully exit the program

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            # print('RecognitionCallback text: ', sentence['text'])

            if RecognitionResult.is_sentence_end(sentence):
                print(
                    '\nRecognitionCallback sentence end, request_id:%s, text: %s'
                    % (result.get_request_id(), sentence['text']))
                self._callback(sentence['text'])

    def on_play_end(self):
        print("play end")

    def on_close(self) -> None:
        print('Recognition close')

class AliyunRecognizer(IRecognition):
    
    def __init__(self, 
            model='paraformer-realtime-v2',
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format='pcm',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=16000,  # supported 8000、16000
            callback=None) -> None:
        super().__init__()
        self.callback = MyRecognitionCallback(callback)
        self.recognition = Recognition(
            model='paraformer-realtime-v2',
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format='pcm',
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=16000,  # supported 8000、16000
            callback=self.callback
        )
        
    def start(self):
        self.recognition.start()
    
    def stop(self):
        self.recognition.stop()
    
    def send_audio_frame(self, frame):
        self.recognition.send_audio_frame(frame)
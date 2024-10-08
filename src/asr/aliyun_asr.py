
from src.asr.base import ASR
from dashscope.audio.asr import (Recognition, RecognitionCallback,
                                 RecognitionResult)

class ASRCallback(RecognitionCallback):
    def __init__(self, callback, asr: ASR):
        super().__init__()
        self._callback = callback
        self.asr = asr

    def on_open(self) -> None:
        print('Recognition open')  # recognition open

    def on_complete(self) -> None:
        print('Recognition complete')  # recognition complete

    def on_error(self, result: RecognitionResult) -> None:
        print('RecognitionCallback task_id: ', result.request_id)
        print('RecognitionCallback error: ', result.message)

    def on_event(self, result: RecognitionResult) -> None:
        sentence = result.get_sentence()
        if 'text' in sentence:
            if RecognitionResult.is_sentence_end(sentence):
                print(
                    '\nRecognitionCallback sentence end, request_id:%s, text: %s'
                    % (result.get_request_id(), sentence['text']))
                self._callback(sentence['text'], self.asr.is_playing)
    def on_close(self) -> None:
        print('Recognition close')

class AliyunASR(ASR):
    
    def __init__(self, 
            model='paraformer-realtime-v2',
            format='pcm',
            sample_rate=16000,
            callback=None,
            api_key=None,
            **kwargs) -> None:
        super().__init__()
        import dashscope
        dashscope.api_key = api_key
        self.callback = ASRCallback(callback, self)
        self.recognition = Recognition(
            model=model,
            # 'paraformer-realtime-v1'、'paraformer-realtime-8k-v1'
            format=format,
            # 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr', you can check the supported formats in the document
            sample_rate=sample_rate,  # supported 8000、16000
            callback=self.callback
        )
        
    def start(self, is_playing):
        super().start(is_playing)
        self.recognition.start()
    
    def stop(self):
        super().stop()
        self.recognition.stop()
    
    def send_audio_frame(self, frame):
        super().send_audio_frame(frame)
        self.recognition.send_audio_frame(frame)
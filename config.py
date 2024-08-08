config = {
    "audio_input": {
        "class": "audio_input.pcm_recorder.PCMRecorder",
        "params": {}
    },
    "recognition": {
        "class": "asr.aliyun_recognition.AliyunRecognition",
        "params": {}
    },
    "model": {
        "class": "llm.aliyun_llm.AliyunLLM",
        "params": {
            "prompt": "Please generate a response for the following input."
        }
    },
    "speech_synthesizer": {
        "class": "tts.aliyun_tts.AliyunTTS",
        "params": {}
    },
    "audio_player": {
        "class": "audio_player.pcm_player.PCMPlayer",
        "params": {}
    }
}
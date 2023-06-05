import os
import azure.cognitiveservices.speech as speechsdk

def recognize_from_microphone():
    
    # azureのAPIキー及びリージョンを入力
    SPEECH_KEY = ""
    SPEECH_REGION = "japanwest" # 日本
    
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_recognition_language="ja-JP"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("メイが待機中....")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        text = speech_recognition_result.text
        return text
 
# for debug
if __name__ == "__main__": 
	print(recognize_from_microphone())
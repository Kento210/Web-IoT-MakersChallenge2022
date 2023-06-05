import openai
import jtalk
import azure_speech
import DeepL_Ja_En
import DeepL_En_Ja
import time
import RPi.GPIO as GPIO
import subprocess
import vlc
import datetime
  
def openai_Talk():
    inputtext = azure_speech.recognize_from_microphone()
    time.sleep(1)
    if "電話をかけて" in inputtext:
        print("私：" + inputtext)
        print("電話をかけるため、電話アプリを起動します")
        jtalk.jtalk("電話をかけるため、電話アプリを起動します")

        gpio_pin7 = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin7, GPIO.OUT)
        GPIO.output(gpio_pin7, True)
        time.sleep(10)
        GPIO.cleanup(gpio_pin7)
    
    elif "BGMをかけて" in inputtext:
        print("私：" + inputtext)
        print("BGMを起動します")
        jtalk.jtalk("BGMを起動します")
        gpio_pin6 = 16
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin6, GPIO.OUT)
        GPIO.output(gpio_pin6, True)
        
        player = vlc.MediaListPlayer()
        mediaList = vlc.MediaList(['bgm.wav'])
        player.set_media_list(mediaList)
        player.set_playback_mode(vlc.PlaybackMode.loop)

        player.play()
        input() #入力待ち
        player.stop()
        GPIO.cleanup(gpio_pin6)

    elif "時刻を教えて" in inputtext:
        print("私：" + inputtext)
        print("現在の時刻：")
        jtalk.jtalk("現在の時刻は、")

        dt_now = datetime.datetime.now()
        now_time_j = dt_now.strftime('%Y年%m月%d日 %H時%M分%S秒')
        print(now_time_j)
        # 2019年02月04日 21:04:15
        jtalk.jtalk(now_time_j + "です。")

    elif "ばか" in inputtext or "バカ" in inputtext or "馬鹿" in inputtext:
        print("私：" + inputtext)
        print("デモ中")
        jtalk.jtalk("理解できません。私の演算能力は53万ですよ！！！！！！！！")
        gpio_pin5 = 20
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio_pin5, GPIO.OUT)
        GPIO.output(gpio_pin5, True)
        time.sleep(5)
        GPIO.cleanup(gpio_pin5)

    else:
        openai_Talk_mein(inputtext)

def openai_Talk_mein(inputtext):
    print("私：" + inputtext)
    API_KEY = "" # OpenAIのAPIキーを指定
    openai.api_key = API_KEY
    f  = open('talk.log', 'r')
    Log = f.read()
    f.close()
    prompt ='''
私：{}
AI：'''.format(inputtext)
    Intext_ja = Log + prompt
    Intext_en =  DeepL_Ja_En.DeepL_ja_en(Intext_ja).text
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=Intext_en,
        max_tokens=200,
        temperature=0.5,
        stop="\n")
    Restext_en = response['choices'][0]['text']
    Restext_ja = DeepL_En_Ja.DeepL_en_ja(Restext_en).text
    print("メイ:" + Restext_ja)
    newLog = Intext_ja + Restext_ja
    f = open('talk.log', 'w')
    f.write(newLog)
    f.close()
    
    jtalk.jtalk(Restext_ja)
    digitClassifier(Restext_ja)

def digitClassifier(Restext_ja):
    text = Restext_ja

    # "喜び："の位置を検索し、その後の数字を取得する
    indexa = text.rfind("喜び")
    placea = indexa + 3
    yorokobi = int(text[placea])
    # "怒り："の位置を検索し、その後の数字を取得する
    indexb = text.rfind("怒り")
    placeb = indexb + 3
    ikari = int(text[placeb])
    # "悲しみ："の位置を検索し、その後の数字を取得する
    indexc = text.rfind("悲しみ")
    placec = indexc + 4
    kanashimi = int(text[placec])
    # "自信："の位置を検索し、その後の数字を取得する
    #index = text.rfind("自信")
    #place = index + 3
    #zishin = int(text[place])

    #print(yorokobi+ikari+kanashimi)

    # GPIO処理
    # GPIOの使用する番号を代入
    gpio_pin1 = 16
    gpio_pin2 = 20
    gpio_pin3 = 21
    gpio_pin4 = 2

    #GPIO番号指定準備
    GPIO.setmode(GPIO.BCM)

    #出力を指定
    GPIO.setup(gpio_pin1, GPIO.OUT)
    GPIO.setup(gpio_pin2, GPIO.OUT)
    GPIO.setup(gpio_pin3, GPIO.OUT)
    GPIO.setup(gpio_pin4, GPIO.OUT)

    #感情処理 受け渡し
    if yorokobi >= 3:
        GPIO.output(gpio_pin1, True)
        GPIO.output(gpio_pin2, False)
        GPIO.output(gpio_pin3, False)
        time.sleep(10)
    elif ikari >= 1:
        GPIO.output(gpio_pin2, True)
        GPIO.output(gpio_pin1, False)
        GPIO.output(gpio_pin3, False)
        time.sleep(10)
    elif kanashimi >= 1:
        GPIO.output(gpio_pin3, True)
        GPIO.output(gpio_pin1, False)
        GPIO.output(gpio_pin2, False)
        time.sleep(10)
    else:
        print("")
    
    #チョコシステム 受け渡し
    if yorokobi >= 3:
         GPIO.output(gpio_pin4, True)
         time.sleep(5)
    else:
         print("")

    #GPIO.output(gpio_pin1, False)
    #GPIO.output(gpio_pin2, False)
    #GPIO.output(gpio_pin3, False)
    #GPIO.output(gpio_pin4, False)

    # 後処理 GPIOを解放
    GPIO.cleanup(gpio_pin1)
    GPIO.cleanup(gpio_pin2)
    GPIO.cleanup(gpio_pin3)
    GPIO.cleanup(gpio_pin4)


if __name__ == "__main__":
	openai_Talk()
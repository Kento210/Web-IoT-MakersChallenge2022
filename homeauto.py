import paho.mqtt.client as mqtt
import json
import time
import multiprocessing
import sys
import OpenAI
import jtalk

TOKEN = "" # beebotteのChannelTokenを指定
HOSTNAME = "mqtt.beebotte.com" # 認証鍵
PORT = 8883
TOPIC = ""
CACERT = "mqtt.beebotte.com.pem"  # mqtt.beebotte.com.pemのパス指定

def on_connect(client, userdata, flags, respons_code):
    print('status {0}'.format(respons_code))
    client.subscribe(TOPIC)

play_thread = None

# ON, OFF時の動作
def on_message(client, userdata, msg):
	data = json.loads(msg.payload.decode("utf-8"))["data"][0]
	cmd = data["comand"]
	if cmd == "Talk_ON":
		time.sleep(3)
		print("こんにちは、私の名前はメイ、お手伝いできることはありますか？\n")
		jtalk.jtalk("こんにちは、私の名前はメイ、お手伝いできることはありますか？")
		print("私で良ければどんな相談にでも乗るから、遠慮なく何でも相談してくださいね")
		jtalk.jtalk("私で良ければ、どんな相談にでも、乗るから、遠慮なくなんでも相談して、くださいね")
		
		if play_thread is not None:
			play_thread.terminate()
		Loop()

	elif cmd == "Talk_OFF":
		print("機能OFF信号を受信しました。また会える日を心待ちにしています！")
		jtalk.jtalk("機能OFF信号を受信しました。また会える日を心待ちにしています！")
		print("あ、「ラズパイを有効にして」ですぐに会えますので、すぐにONにしてもいいんですよ？")
		jtalk.jtalk("あ、「アシスタントを有効にして」ですぐに会えますので、すぐにONにしてもいいんですよ？")
		play_thread.terminate()

def Loop():
	global play_thread
	play_thread = multiprocessing.Process(target = AITalk)
	play_thread.start()

def AITalk():
	while True:
		OpenAI.openai_Talk()

client = mqtt.Client()
client.username_pw_set("token:%s"%TOKEN)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(CACERT)
client.connect(HOSTNAME, port=PORT, keepalive=60)
client.loop_forever()
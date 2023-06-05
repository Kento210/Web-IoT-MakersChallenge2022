# Web-IoT-MakersChallenge2022
2022年度開催のWeb×IoTメイカーズチャレンジで制作を行ったもの

<h3>azure_speech.py</h3>
<p>
azureによる声の文字起こしを実行する
</p>

<h3>DeepL_En_Ja.py</h3>
<p>
DeepL APIを使用し、英語を日本語に翻訳する<br>
本システムではユーザに返す前にChatGPT APIから受け取ったものを翻訳している。
</p>

<h3>DeepL_Jp_En.py</h3>
<p>
DeepL APIを使用し、日本語を英語に翻訳する<br>
本システムではユーザから受け取ったデータを翻訳し、渡すことで精度を高めている
</p>

<h3>homeauto.py</h3>
<p>
Google HomeとIFTTTを使用した遠隔ON, OFFを実装している
</p>

<h3>jtalk.py</h3>
<p>
Open jtalk (ラズパイでの音声出力用ライブラリ)の設定ファイル
</p>

<h3>OpenAI.py</h3>
<p>
メイン部分、AIによる応答の実行とそれによるAIの感情の出力、チョコシステムの動作をGPIOで制御している
</p>

<h3>talk.log</h3>
<p>
簡易記憶として保存するログ、Mayはここに記憶を保持し、毎回読み込むことで過去の対話をリマインドする。
</p>


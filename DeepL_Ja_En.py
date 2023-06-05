import deepl

def DeepL_ja_en(inputtext):
	API_KEY = '' # DeepLのAPIキーを指定
	text = inputtext
	source_lang = 'JA'
	target_lang = 'EN-US'

	# イニシャライズ
	translator = deepl.Translator(API_KEY)

	# 翻訳を実行
	result = translator.translate_text(text, source_lang=source_lang, target_lang=target_lang)
	return result

if __name__ == "__main__": 
	print(DeepL_ja_en("こんにちは"))
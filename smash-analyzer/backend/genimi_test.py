import os
from google.generativeai import text

# APIキーの設定 (環境変数から取得)
os.environ["GOOGLE_API_KEY"] = "***REMOVED***" # 取得したAPIキーを設定

# テキスト生成モデルの初期化
model = text.Model("models/gemini-pro")

# プロンプトの作成
prompt = "Hello, Gemini!"

# テキスト生成の実行
response = model.generate_text(prompt=prompt)

# 結果の表示
print(response.result)
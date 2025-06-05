# 🎮 SSBU Analyze - 大乱闘スマッシュブラザーズ分析ツール

**SSBU Analyze** は、大乱闘スマッシュブラザーズ（Smash Bros. Ultimate）のプレイデータや画像を解析し、プレイヤー行動の可視化や最適なアクション提案を行う分析支援アプリです。

---

## 🔍 主な機能

- 📸 撮影画像のアップロードからプレイ内容を解析
- 📊 キャラクターの行動パターンの可視化
- 🤖 AIによる次の最適行動レコメンド
- 📁 分類済データからキャラ別の傾向分析
- 🧠 GeminiやVision APIとの連携（予定）

---

## 🧰 使用技術

- Python（Flask / FastAPI）
- OpenCV / PIL
- SQLite（簡易DB）
- HTML / CSS / JavaScript
- Google Cloud Vision API（予定 or 実装済）
- Git / GitHub

---

## 📁 ディレクトリ構成

```

ssbu\_analyze/
├── cloud-run/               # デプロイ用の構成（Dockerfileなど）
├── smash-analyzer/          # 分析ロジック・UI
│   ├── backend/             # Pythonスクリプト群
│   ├── css/                 # スタイリング
│   ├── js/                  # フロントJS
│   └── index.html           # UI画面
├── .gitignore
├── README.md
└── requirements.txt

````

---

## 🚀 セットアップ方法

1. リポジトリをクローン

```bash
git clone https://github.com/takaaaaaayuki/ssbu_analyze.git
cd ssbu_analyze
````

2. 仮想環境の作成（任意）

```bash
python -m venv venv
source venv/bin/activate
```

3. 必要パッケージをインストール

```bash
pip install -r requirements.txt
```

4. アプリを起動

```bash
python app.py
# または
uvicorn app:app --reload
```

---

## 🧪 今後の予定

* Gemini APIを使った行動提案機能の拡張
* プレイヤー別の分析結果保存＆比較
* データアップロードによるモデル学習強化
* Web UI の改善（Tailwind CSS適用予定）

---

## 👨‍💻 開発・保守

* 開発者：[@takaaaaaayuki](https://github.com/takaaaaaayuki)

---



# 🎮 SSBU Analyze - 大乱闘スマッシュブラザーズ SPECIAL 最適化行動支援システム

[▶️ YouTubeデモ](https://youtu.be/V89e8IKk7L8)  
[🌐 公開アプリURL](https://smash-analyzer-dtbx5ymvvq-an.a.run.app/)

---

## 📘 概要

**SSBU Analyze** は、人気対戦アクションゲーム『大乱闘スマッシュブラザーズ SPECIAL（スマブラSP）』におけるプレイヤーの立ち回りをサポートする分析支援ツールです。画像処理・AI・座標計算を通じて、プレイヤーに最適な次の行動を提案します。

---

## 🧩 主な機能

- 撮影画像をアップロードして状況を数値化
- キャラクターの位置座標をマス目ベースで計算
- SQLiteデータベースに登録されたキャラ技情報から適切な技を判定
- Google Gemini API を活用したチャット形式の行動提案生成
- プレイヤー・相手の距離/ダメージ/座標を元に有利不利を判断し行動を助言

---

## 🧠 システム構成

### ユーザー層（フロントエンド）

- Web UI（HTML/CSS/JavaScript）で画像アップロード、座標クリック、チャット機能を提供
- JavaScript によるマス目クリック座標の取得＆送信

### サーバー層（バックエンド）

- FastAPI によるエンドポイント管理
- 座標計算、距離評価、行動推定のロジックを内包
- Gemini API による自然言語出力生成

### データストア

- `smash_characters.db`：キャラ別に技、射程、ダメージ、発生フレーム等を登録済みのSQLite DB
- アップロード画像の保存と分析結果の保持

---

## 💻 使用技術

- Python（FastAPI / OpenCV / SQLite）
- Google Gemini API
- HTML / CSS / JavaScript
- Cloud Run（デプロイ先）

---

## 🧪 分析アルゴリズム概要

1. 入力画像を33×16のグリッドに分割
2. ユーザーがクリックでキャラ位置を指定
3. 座標距離とダメージ値を元に戦況を評価
4. Gemini APIに状況を投げて、次に取るべき行動・戦略を文章で出力

---

## 📂 ディレクトリ構成（抜粋）

```

ssbu\_analyze/
├── smash-analyzer/
│   ├── backend/           # Python画像処理・分析ロジック
│   ├── css/               # スタイリング
│   └── js/                # ユーザー操作と送信処理
├── cloud-run/             # デプロイ用Docker構成
├── smash\_characters.db    # 技・射程・データDB
├── .gitignore
└── README.md

```

---

## 🔮 今後の展望

- 全87キャラへの対応
- 各ステージ対応（例：戦場、小戦場）
- 動画入力によるリアルタイム戦況分析
- Geminiチャットの精度向上＆マッチアップ学習機能の実装

---

## 👤 開発

- 開発・設計・フロント・AI構築・文章生成すべて担当  
- GitHub: [@takaaaaaayuki](https://github.com/takaaaaaayuki)

---

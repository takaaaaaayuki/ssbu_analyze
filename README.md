# 🎮 SSBU Analyze - 大乱闘スマッシュブラザーズ SPECIAL最適化行動システム

[▶️ YouTube Demo](https://youtu.be/V89e8IKk7L8)  
[🌐 Web App Link](https://smash-analyzer-dtbx5ymvvq-an.a.run.app/)

---

## 🔍 概要

**SSBU Analyze** は、「大乱闘スマッシュブラザーズ SPECIAL」における戦略性の高さ・技術習得の難しさを、AIと画像処理によってサポートする分析支援システムです。  
プレイヤーの現在状況に応じて、最適な立ち回りや技選択を自動提案します。

---

## 📐 システム構成図

![図](/mnt/data/スクリーンショット 2025-06-05 23.05.22.png)

---

## 📸 画像処理結果例（グリッド分割 × 座標解析）

画像をマス目に分割し、プレイヤー・相手キャラの位置を数値化、距離を算出します。

![図](/mnt/data/スクリーンショット 2025-06-05 23.05.38.png)

---

## 🤖 Gemini AIによる行動提案の出力結果例

現在の状況や座標・ダメージ・距離に応じて、Gemini AIが次の行動を論理的に説明します。

![図](/mnt/data/スクリーンショット 2025-06-05 23.06.15.png)

---

## 🧠 システムの特徴と実装

### 🔸 目的

- ゲーム上達の効率化
- AIによる立ち回り提案
- 画像を用いた戦況の数値化・分析

---

### 🔸 主な機能

- マス目単位でのグリッド分割
- キャラクターのクリック検出 → 座標化
- 相対距離の自動計算
- キャラごとの技射程・特性データベース
- Gemini APIを活用した行動提案
- AIによる「ジャンプ or 回避 or 攻撃」の推奨判断

---

### 🔸 使用技術

- Python（Flask / FastAPI）
- OpenCV / PIL
- SQLite3
- Google Gemini API（プロンプト最適化）
- HTML / JavaScript / CSS

---

## 🗂️ ディレクトリ構成（抜粋）

```

ssbu\_analyze/
├── smash-analyzer/           # Web UIとJS、静的ファイル
│   ├── backend/              # Flaskアプリ・画像処理ロジック
│   ├── css/                  # スタイル
│   └── js/                   # ユーザー操作 & 座標送信
├── cloud-run/                # Cloud Run 用 Dockerfile 等
├── smash\_characters.db       # キャラクター技データベース
└── README.md

```

---

## 🔬 分析モデル詳細

- グリッドは**横33×縦16分割**
- 画像クリックでマリオ＆リンクの座標を取得
- 距離算出とキャラの蓄積ダメージに基づき、有利不利を分類
- Gemini APIがプロンプトを生成・チャット出力

---

## 🎯 今後の展望

- キャラ追加（87体全員対応）
- ステージごとの最適化
- リアルタイム戦闘支援（動画分析）
- コミュニティとの連携によるAI改善

---

## 👤 開発担当 
- 開発・設計・フロント・AI設計すべて担当  
- Contact: [GitHub Profile](https://github.com/takaaaaaayuki)

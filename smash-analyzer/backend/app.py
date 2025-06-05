#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
app.py

【機能まとめ】
1) ImageAnalyzerクラスで:
   - Geminiモデルを使って画像説明・チャット生成
2) Flaskアプリで:
   - 画像をアップロードしてマス目を描画 (draw_grid.pyを使用)
   - ユーザーが画像を2回クリック → 距離計算
   - DBから各キャラの推奨行動を取得 (recommend_actions)
   - Gemini API を使い、トップ5推奨行動とコメントを自然言語で回答
   - ユーザーと対話できるチャット機能 (/api/chat)
   
【使い方】
  1. cd path/to/zen_hackathon/smash-analyzer/backend
  2. pip install flask pillow google-generativeai python-dotenv
  3. .envファイルに GOOGLE_API_KEY を設定する
  4. 必要な smash_characters.db と draw_grid.py を配置する
  5. python app.py を実行
  6. ブラウザで http://127.0.0.1:7000/ にアクセス
"""

import os
import io
import uuid
import sqlite3

from dotenv import load_dotenv
from flask import Flask, request, render_template_string, jsonify, url_for
from PIL import Image
import google.generativeai as genai

# draw_grid.py からマス目描画関数をインポート
from draw_grid import draw_grid_with_relative_coords

###############################################################################
# .envの読み込み (GOOGLE_API_KEYなど)
###############################################################################
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("環境変数 GOOGLE_API_KEY が設定されていません (.env を確認してください)")

###############################################################################
# Gemini API の初期化
###############################################################################
genai.configure(api_key=API_KEY)

###############################################################################
# Geminiのみを利用する ImageAnalyzer クラス
###############################################################################
class ImageAnalyzer:
    def __init__(self):
        # ※ モデル名は環境に合わせて調整してください
        self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_with_gemini(self, image_path, prompt="この画像について詳しく説明してください。"):
        img = Image.open(image_path)
        response = self.gemini_model.generate_content([prompt, img])
        return response.text

    def comprehensive_analysis(self, image_path):
        gemini_description = self.analyze_with_gemini(image_path)
        return {'Geminiによる説明': gemini_description}

###############################################################################
# DBから推奨行動を取得する関数
# 各テーブルの全行について、数値カラムで distance <= 値 のものを抽出
###############################################################################
def recommend_actions(db_path, character_id, distance):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    tables = ["B_moves", "air_moves", "dash_moves", "kyou_zyaku_moves", "smash_moves", "throw_moves"]
    recommended = []
    for table in tables:
        c.execute(f"SELECT * FROM {table} WHERE character_id=?", (character_id,))
        rows = c.fetchall()
        if not rows:
            continue
        for row in rows:
            columns = row.keys()
            for col in columns:
                if col in ("id", "character_id"):
                    continue
                val = row[col]
                if val is None or not isinstance(val, (int, float)):
                    continue
                if distance <= val:
                    recommended.append((table, col, val))
    conn.close()
    return recommended

def get_top5_moves(recommended_list):
    if not recommended_list:
        return []
    sorted_list = sorted(recommended_list, key=lambda x: x[2])
    return sorted_list[:5]

###############################################################################
# Flaskアプリ設定
###############################################################################
app = Flask(__name__, static_folder="images")
IMAGES_FOLDER = os.path.join(app.root_path, "images")
os.makedirs(IMAGES_FOLDER, exist_ok=True)

DB_PATH = "smash_characters.db"

# グローバルにクリック情報を管理する辞書
click_data_storage = {}

# 対話用の会話履歴グローバル辞書（会話IDをキーに）
conversation_history = {}

# UI部分：スタイルを水色と赤を基調に、エフェクトやロード中表示も追加
HTML_FORM = """
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Gemini+マス目座標アプリ</title>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #e0f7fa; /* 水色の薄い背景 */
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 900px;
      margin: 30px auto;
      background-color: #ffffff;
      padding: 20px 30px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15);
      border-radius: 10px;
    }
    h1, h2 {
      color: #d32f2f; /* 赤系のタイトル */
      text-align: center;
    }
    form {
      margin-bottom: 20px;
    }
    label {
      display: block;
      margin: 10px 0 5px;
      font-weight: bold;
      color: #1565c0; /* 水色系のテキスト */
    }
    input[type="number"],
    input[type="text"],
    input[type="file"],
    select {
      width: 100%;
      padding: 10px;
      margin-bottom: 10px;
      border: 1px solid #90caf9;
      border-radius: 4px;
      box-sizing: border-box;
    }
    button {
      padding: 10px 20px;
      background-color: #d32f2f;
      color: #ffffff;
      border: none;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
    }
    button:hover {
      background-color: #b71c1c;
    }
    img {
      display: block;
      max-width: 100%;
      margin: 20px auto;
      border: 3px solid #1565c0;
      border-radius: 6px;
    }
    #click-info, #distance-result, #chat-history {
      background-color: #bbdefb;
      padding: 10px;
      border-radius: 4px;
      margin: 10px 0;
    }
    /* ローディングエフェクト用のスタイル */
    .loader {
      border: 4px solid #f3f3f3;
      border-top: 4px solid #d32f2f;
      border-radius: 50%;
      width: 30px;
      height: 30px;
      animation: spin 1s linear infinite;
      display: inline-block;
      vertical-align: middle;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    #chatForm input[type="text"] {
      width: 75%;
      display: inline-block;
      margin-right: 10px;
    }
    #chatForm button {
      width: 20%;
    }
  </style>
</head>
<body>
<div class="container">
  <h1>Gemini+マス目座標アプリ</h1>
  <form method="POST" enctype="multipart/form-data">
    <label>画像を選択:</label>
    <input type="file" name="image_file" accept="image/*" required>
    <label>縦方向(列)のマス数 (columns):</label>
    <input type="number" name="columns" value="33" required>
    <label>横方向(行)のマス数 (rows):</label>
    <input type="number" name="rows" value="16" required>
    <label>原点(0,0)にしたいマス番号 (origin_cell):</label>
    <input type="number" name="origin_cell" value="347" required>
    <label>線と文字の色 (R G B):</label>
    <input type="text" name="line_color" value="255,255,255">
    <label>線の太さ (line_width):</label>
    <input type="number" name="line_width" value="1">
    <button type="submit">送信する</button>
  </form>
  {% if output_filename %}
  <hr>
  <h2>生成結果</h2>
  <p>画像上で2回クリックしてください。<br>
     <span id="loading-message" style="color: #d32f2f; font-weight: bold; display: none;">ロード中...</span>
  </p>
  <img id="clickable-image" src="{{ url_for('static', filename=output_filename) }}" alt="Result Image">
  <div id="click-info"></div>
  <form id="characterForm">
    <label>1回目のクリックはどのキャラか:</label>
    <select name="char1">
      <option value="Mario">Mario</option>
      <option value="Link">Link</option>
      <option value="Unknown">Unknown</option>
    </select>
    <label>2回目のクリックはどのキャラか:</label>
    <select name="char2">
      <option value="Mario">Mario</option>
      <option value="Link">Link</option>
      <option value="Unknown">Unknown</option>
    </select>
    <button type="button" onclick="submitCharacter()">距離を計算＋AI回答</button>
  </form>
  <div id="distance-result"></div>
  <hr>
  <h2>Geminiチャット対話</h2>
  <form id="chatForm">
    <input type="text" id="chatInput" placeholder="メッセージを入力してください">
    <button type="button" onclick="sendChat()">送信</button>
    <span id="chat-loading" class="loader" style="display:none;"></span>
  </form>
  <div id="chat-history"></div>
  {% endif %}
</div>
<script>
  let clickCount = 0;
  const clickInfoDiv = document.getElementById('click-info');
  const imgEl = document.getElementById('clickable-image');
  const randomKey = "{{ random_key }}";
  if (imgEl) {
    imgEl.addEventListener('click', function(e) {
      const rect = imgEl.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      clickCount++;
      fetch('/api/record_click', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ random_key: randomKey, click_number: clickCount, x: x, y: y })
      })
      .then(res => res.json())
      .then(data => { console.log('Server response:', data); })
      .catch(err => console.error(err));
      clickInfoDiv.innerHTML = `クリック${clickCount}: (x=${x}, y=${y})<br>` + clickInfoDiv.innerHTML;
    });
  }
  function submitCharacter() {
    const distanceResultDiv = document.getElementById('distance-result');
    distanceResultDiv.innerHTML = "<div class='loader'></div> 計算中...";
    const formEl = document.getElementById('characterForm');
    const formData = new FormData(formEl);
    const char1 = formData.get('char1');
    const char2 = formData.get('char2');
    fetch('/api/calc_distance', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ random_key: randomKey, char1: char1, char2: char2 })
    })
    .then(res => res.json())
    .then(data => {
       if (data.message) {
           distanceResultDiv.innerHTML = data.message;
       }
    })
    .catch(err => {
      console.error(err);
      distanceResultDiv.innerHTML = "エラーが発生しました。";
    });
  }
  function sendChat() {
    const chatLoading = document.getElementById('chat-loading');
    const chatHistoryDiv = document.getElementById('chat-history');
    const chatInput = document.getElementById('chatInput');
    const userMessage = chatInput.value;
    chatInput.value = "";
    chatLoading.style.display = "inline-block";
    fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: "{{ random_key }}", message: userMessage })
    })
    .then(res => res.json())
    .then(data => {
      chatLoading.style.display = "none";
      chatHistoryDiv.innerHTML += "<p><b>ユーザー:</b> " + userMessage + "</p>";
      chatHistoryDiv.innerHTML += "<p><b>Gemini:</b> " + data.answer + "</p>";
    })
    .catch(err => {
      console.error(err);
      chatLoading.style.display = "none";
    });
  }
</script>
</body>
</html>
"""

###############################################################################
# Flaskルート
###############################################################################
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image_file")
        columns = int(request.form.get("columns", 33))
        rows = int(request.form.get("rows", 16))
        origin_cell = int(request.form.get("origin_cell", 347))
        line_color_str = request.form.get("line_color", "255,255,255")
        line_width = int(request.form.get("line_width", 1))
        try:
            r, g, b = map(int, line_color_str.split(","))
            line_color = (r, g, b)
        except:
            line_color = (255,255,255)
        if file:
            ext = os.path.splitext(file.filename)[1]
            random_key = uuid.uuid4().hex[:8]
            input_filename = f"input_{random_key}{ext}"
            output_filename = f"output_{random_key}{ext}"
            input_path = os.path.join(IMAGES_FOLDER, input_filename)
            output_path = os.path.join(IMAGES_FOLDER, output_filename)
            file.save(input_path)
            draw_grid_with_relative_coords(
                image_path=input_path,
                output_path=output_path,
                columns=columns,
                rows=rows,
                origin_cell=origin_cell,
                line_color=line_color,
                line_width=line_width
            )
            click_data_storage[random_key] = {
                "input_path": input_path,
                "output_path": output_path,
                "columns": columns,
                "rows": rows,
                "origin_cell": origin_cell,
                "clicks": []
            }
            conversation_history[random_key] = []
            return render_template_string(HTML_FORM, output_filename=output_filename, random_key=random_key)
    return render_template_string(HTML_FORM)

@app.route("/api/record_click", methods=["POST"])
def record_click():
    data = request.get_json()
    random_key = data.get("random_key")
    click_number = data.get("click_number")
    x = data.get("x")
    y = data.get("y")
    if random_key not in click_data_storage:
        return jsonify({"error": "Invalid random_key"}), 400
    click_info = {"click_number": click_number, "x": x, "y": y}
    click_data_storage[random_key]["clicks"].append(click_info)
    return jsonify({"status": "ok", "message": "クリック座標を保存したします！"})

@app.route("/api/calc_distance", methods=["POST"])
def calc_distance():
    """
    2回クリックの座標からマス目上の距離を計算し、
    DBから各キャラの推奨行動（トップ5）を取得、
    さらにGemini APIで画像コメントを生成して返すAPI
    """
    data = request.get_json()
    random_key = data.get("random_key")
    char1 = data.get("char1")
    char2 = data.get("char2")
    char_map = {"Mario": 1, "Link": 2, "Unknown": 0}
    char1_id = char_map.get(char1, 0)
    char2_id = char_map.get(char2, 0)
    if random_key not in click_data_storage:
        return jsonify({"message": "random_keyが不正します"}), 400
    stored_data = click_data_storage[random_key]
    clicks = stored_data["clicks"]
    if len(clicks) < 2:
        return jsonify({"message": "クリックが2回未満します"}), 400
    columns = stored_data["columns"]
    rows = stored_data["rows"]
    origin_cell = stored_data["origin_cell"]
    with Image.open(stored_data["input_path"]) as im:
        width, height = im.size
    cell_width = width / columns
    cell_height = height / rows
    origin_index = origin_cell - 1
    origin_row = origin_index // columns
    origin_col = origin_index % columns
    clicks_sorted = sorted(clicks, key=lambda c: c["click_number"])
    x1, y1 = clicks_sorted[0]["x"], clicks_sorted[0]["y"]
    x2, y2 = clicks_sorted[1]["x"], clicks_sorted[1]["y"]
    col1 = int(x1 // cell_width)
    row1 = int(y1 // cell_height)
    col2 = int(x2 // cell_width)
    row2 = int(y2 // cell_height)
    rel_x1 = col1 - origin_col
    rel_y1 = row1 - origin_row
    rel_x2 = col2 - origin_col
    rel_y2 = row2 - origin_row
    cell_num1 = row1 * columns + col1 + 1
    cell_num2 = row2 * columns + col2 + 1
    dx = rel_x2 - rel_x1
    dy = rel_y2 - rel_y1
    dist = (dx**2 + dy**2) ** 0.5

    recommended1 = recommend_actions(DB_PATH, char1_id, dist)
    top5_1 = get_top5_moves(recommended1)
    recommended2 = recommend_actions(DB_PATH, char2_id, dist)
    top5_2 = get_top5_moves(recommended2)

    def moves_to_html(moves):
        if not moves:
            return "(該当なし)"
        return "<ul>" + "".join(f"<li>{tbl} の {clm} <= {val}</li>" for (tbl, clm, val) in moves) + "</ul>"

    # ここで、Geminiへの質問プロンプトを作成（基本的な状況分析に基づく）
    situation_prompt = f"""
スマッシュブラザーズの対戦状況を分析してください。
プレイヤー: {char1}
  マス番号: {cell_num1}
  相対座標: ({rel_x1}, {rel_y1})
対戦相手: {char2}
  マス番号: {cell_num2}
  相対座標: ({rel_x2}, {rel_y2})
システムの推奨行動:
{moves_to_html(top5_1)} (for {char1})
{moves_to_html(top5_2)} (for {char2})
ユークリッド距離: {dist:.2f} (マス単位)
上記の情報に基づいて、最も効果的な戦略とその理由を具体的に提案してください。
"""
    analyzer = ImageAnalyzer()
    gemini_explanation = analyzer.analyze_with_gemini(stored_data["input_path"], prompt=situation_prompt)
    
    msg = f"""
    [1回目クリック] {char1} → ピクセル({x1:.1f},{y1:.1f}) → マス {cell_num1} → 相対({rel_x1},{rel_y1})<br>
    [2回目クリック] {char2} → ピクセル({x2:.1f},{y2:.1f}) → マス {cell_num2} → 相対({rel_x2},{rel_y2})<br>
    <br>
    ユークリッド距離 = {dist:.2f} (マス単位)<br><br>
    <b>{char1} のTop5推奨行動</b>: {moves_to_html(top5_1)}<br>
    <b>{char2} のTop5推奨行動</b>: {moves_to_html(top5_2)}<br><br>
    <hr>
    <b>Geminiからのコメント</b>:<br>
    {gemini_explanation}
    """
    return jsonify({"message": msg})

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    ユーザーからのメッセージを受け取り、対話形式でGeminiに質問するAPI。
    会話履歴はグローバルな conversation_history に保存する。
    """
    data = request.get_json()
    conversation_id = data.get("conversation_id")
    user_message = data.get("message")
    if not conversation_id:
        conversation_id = uuid.uuid4().hex
        conversation_history[conversation_id] = []
    if conversation_id not in conversation_history:
        conversation_history[conversation_id] = []
    conversation_history[conversation_id].append({"role": "user", "content": user_message})
    context = "\n".join(f"{msg['role']}: {msg['content']}" for msg in conversation_history[conversation_id])
    prompt = f"以下の対話履歴を参考にして回答してください。\n{context}\nassistant:"
    response = genai.GenerativeModel('gemini-1.5-flash').generate_content([prompt])
    answer = response.text
    conversation_history[conversation_id].append({"role": "assistant", "content": answer})
    return jsonify({"conversation_id": conversation_id, "answer": answer})

if __name__ == "__main__":
    print("Flaskを起動するします！！！ http://127.0.0.1:7000/ にアクセスしてほしいします！！！")
    app.run(debug=True, host="127.0.0.1", port=7000)

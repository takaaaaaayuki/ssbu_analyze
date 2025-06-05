#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
draw_grid.py

指定した画像に縦横のマス目を描画しつつ、
任意のマス番号を(0,0)とする座標を画像上に描画してくれるスクリプトします！！！

【特徴】
- 入力画像は「images」フォルダの中に置く
- 出力画像は「images/output_{ランダム文字列}.jpg」という名前で自動生成
- columns, rows, origin_cell, line_color, line_width はオプションで調整できるします！！！

【実行例】
  python draw_grid.py \
    --input_image test.jpg \
    --columns 33 \
    --rows 16 \
    --origin_cell 347 \
    --line_color 255 255 255 \
    --line_width 1

上記コマンドを実行すると、
images/test.jpg を読み込んで
images/output_xxxxxxxx.jpg（xxxxxxxx=ランダム文字列）で出力されるします！！！
"""

import argparse
import os
import uuid
from PIL import Image, ImageDraw, ImageFont

def draw_grid_with_relative_coords(
    image_path, 
    output_path, 
    columns=33, 
    rows=16, 
    origin_cell=347,
    line_color=(255, 255, 255),
    line_width=1
):
    """
    画像に格子を引き、各マスに対して:
    - マス番号
    - origin_cellを(0,0)とした相対座標
    を描画する関数します！！！

    image_path: 入力画像ファイル (例: "images/test.jpg")
    output_path: 出力画像ファイル (例: "images/output_XXXXXX.jpg")
    columns: 縦方向のマス数
    rows: 横方向のマス数
    origin_cell: 原点(0,0)にしたいマス番号
    line_color: 線と文字の色 (R, G, B)
    line_width: 線の太さ
    """
    
    # 画像を読み込み
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    
    # マスの幅・高さ
    cell_width = width / columns
    cell_height = height / rows
    
    # 格子線を描画
    for col in range(columns + 1):
        x = int(col * cell_width)
        draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
    
    for row in range(rows + 1):
        y = int(row * cell_height)
        draw.line([(0, y), (width, y)], fill=line_color, width=line_width)
    
    # フォントを取得
    font = ImageFont.load_default()
    
    # origin_cell(例:347)の行・列を求める
    origin_index = origin_cell - 1
    origin_row = origin_index // columns
    origin_col = origin_index % columns
    
    # 全マスに対してラベルを描画
    for r in range(rows):
        for c in range(columns):
            cell_index = r * columns + c + 1
            rel_x = c - origin_col
            rel_y = r - origin_row
            
            # 表示文字: マス番号 + (相対座標)
            label_text = f"{cell_index} ({rel_x}, {rel_y})"
            
            # テキストサイズ(getmaskで取得)
            mask = font.getmask(label_text)
            text_width, text_height = mask.size
            
            # マス中央にテキストを配置
            text_x = int(c * cell_width + (cell_width - text_width) / 2)
            text_y = int(r * cell_height + (cell_height - text_height) / 2)
            
            draw.text((text_x, text_y), label_text, fill=line_color, font=font)
    
    # 出力先に保存
    img.save(output_path)
    
    # 画像を自動で開いて可視化(環境によっては開かない場合もあるします)
    try:
        img.show()
    except:
        pass


def main():
    parser = argparse.ArgumentParser(description="画像に格子を描画し、指定マスを(0,0)とした座標を加えて保存するスクリプトします！！！")
    parser.add_argument("--input_image", type=str, default="test.jpg", help="入力画像ファイル名 (imagesフォルダ内) します！！！")
    parser.add_argument("--columns", type=int, default=33, help="縦方向(列)のマス数を指定するします！！！")
    parser.add_argument("--rows", type=int, default=16, help="横方向(行)のマス数を指定するします！！！")
    parser.add_argument("--origin_cell", type=int, default=347, help="このマスを(0,0)にしたいします！！！")
    parser.add_argument("--line_color", nargs=3, type=int, default=[255, 255, 255], help="線・文字の色(R G B)を指定してほしいします！！！")
    parser.add_argument("--line_width", type=int, default=1, help="線の太さを指定してほしいします！！！")
    
    args = parser.parse_args()
    
    # 画像を置くフォルダ
    images_folder = "images"
    # フォルダがなければ作る
    os.makedirs(images_folder, exist_ok=True)
    
    # 入力画像のパス (imagesフォルダ内)
    input_path = os.path.join(images_folder, args.input_image)
    
    # ランダムなファイル名を生成 (UUIDの先頭8文字を利用)
    random_key = uuid.uuid4().hex[:8]
    output_filename = f"output_{random_key}.jpg"
    output_path = os.path.join(images_folder, output_filename)

    # 描画処理
    draw_grid_with_relative_coords(
        image_path=input_path,
        output_path=output_path,
        columns=args.columns,
        rows=args.rows,
        origin_cell=args.origin_cell,
        line_color=tuple(args.line_color),
        line_width=args.line_width
    )

    print("処理が完了したで！！！")
    print(f"入力: {input_path} !!!")
    print(f"出力: {output_path} !!!")

if __name__ == "__main__":
    main()

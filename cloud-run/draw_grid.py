from PIL import Image, ImageDraw, ImageFont
import os
import math

def create_font(size=20):  # フォントサイズを大きく
    return ImageFont.load_default()

def draw_grid_with_relative_coords(
    image_path,
    output_path,
    columns=33,
    rows=16,
    origin_cell=347,
    line_color=(255, 255, 255),
    line_width=2,  # 線を太く
    show_cell_numbers=True  # 新しいパラメータ
):
    with Image.open(image_path) as img:
        if img.mode != 'RGB':
            img = img.convert('RGB')
        width, height = img.size
        cell_width = width / columns
        cell_height = height / rows

        # 画像の暗さを軽減（透明度を下げる）
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 40))  # 透明度を半分に減らす
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        draw = ImageDraw.Draw(img)
        font = create_font()
        
        origin_index = origin_cell - 1
        origin_row = origin_index // columns
        origin_col = origin_index % columns

        # グリッド線を描画
        for i in range(columns + 1):
            x = i * cell_width
            draw.line([(x, 0), (x, height)], fill=line_color, width=line_width)
        for i in range(rows + 1):
            y = i * cell_height
            draw.line([(0, y), (width, y)], fill=line_color, width=line_width)

        # マス目情報を描画
        for row in range(rows):
            for col in range(columns):
                center_x = (col + 0.5) * cell_width
                center_y = (row + 0.5) * cell_height
                cell_number = row * columns + col + 1
                rel_x = col - origin_col
                rel_y = row - origin_row

                # 座標を表示
                coord_text = f"({rel_x},{rel_y})"
                coord_width_px = font.getsize(coord_text)[0]

                # サイズ計算
                text_height = 30  # 高さを増やして余裕を持たせる

                # セル番号の処理
                if show_cell_numbers:
                    cell_text = str(cell_number)
                    cell_width_px = font.getsize(cell_text)[0]
                    text_width = max(cell_width_px, coord_width_px)

                    # マス番号を描画
                    draw.text(
                        (center_x - cell_width_px/2, center_y - text_height),
                        cell_text,
                        fill=line_color,
                        font=font
                    )
                else:
                    # 座標のみを描画
                    draw.text(
                        (center_x - coord_width_px/2, center_y - text_height/6),
                        coord_text,
                        fill=line_color,
                        font=font
                    )

        img.save(output_path, quality=95)

if __name__ == "__main__":
    draw_grid_with_relative_coords(
        image_path="input.jpg",
        output_path="output.jpg",
        columns=33,
        rows=16,
        origin_cell=347,
        line_color=(255, 255, 255),
        line_width=2,
        show_cell_numbers=False  # デフォルトでマス番号を非表示に
    )
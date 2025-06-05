import sqlite3

def create_smash_db():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   # キャラ情報
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS characters (
       id INTEGER PRIMARY KEY,
       name TEXT NOT NULL,
       size_x FLOAT,
       size_y FLOAT,
       weight INTEGER
   )''')

   # 空中攻撃
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS air_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       uair_x FLOAT,
       uair_y FLOAT,
       uair_damage INTEGER,
       uair_startup INTEGER,
       uair_weapon FLOAT,
       fair_x FLOAT,
       fair_y FLOAT,
       fair_damage INTEGER,
       fair_startup INTEGER,
       fair_weapon FLOAT,
       dair_x FLOAT,
       dair_y FLOAT,
       dair_damage INTEGER,
       dair_startup INTEGER,
       dair_weapon FLOAT,
       bair_x FLOAT,
       bair_y FLOAT,
       bair_damage INTEGER,
       bair_startup INTEGER,
       bair_weapon FLOAT,
       nair_x FLOAT,
       nair_y FLOAT,
       nair_damage INTEGER,
       nair_startup INTEGER,
       nair_weapon FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')

   # B技
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS B_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       up_b_x FLOAT,
       up_b_y FLOAT,
       up_b_damage INTEGER,
       up_b_startup INTEGER,
       up_b_weapon FLOAT,
       up_b_tobi FLOAT,
       side_b_x FLOAT,
       side_b_y FLOAT,
       side_b_damage INTEGER,
       side_b_startup INTEGER,
       side_b_weapon FLOAT,
       side_b_tobi FLOAT,
       down_b_x FLOAT,
       down_b_y FLOAT,
       down_b_damage INTEGER,
       down_b_startup INTEGER,
       down_b_weapon FLOAT,
       down_b_tobi FLOAT,
       neutral_b_x FLOAT,
       neutral_b_y FLOAT,
       neutral_b_damage INTEGER,
       neutral_b_startup INTEGER,
       neutral_b_weapon FLOAT,
       neutral_b_tobi FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')

   # 強・弱攻撃
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS kyou_zyaku_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       ftilt_x FLOAT,
       ftilt_y FLOAT,
       ftilt_damage INTEGER,
       ftilt_startup INTEGER,
       ftilt_weapon FLOAT,
       dtilt_x FLOAT,
       dtilt_y FLOAT,
       dtilt_damage INTEGER,
       dtilt_startup INTEGER,
       dtilt_weapon FLOAT,
       utilt_x FLOAT,
       utilt_y FLOAT,
       utilt_damage INTEGER,
       utilt_startup INTEGER,
       utilt_weapon FLOAT,
       jab_x FLOAT,
       jab_y FLOAT,
       jab_damage INTEGER,
       jab_startup INTEGER,
       jab_weapon FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')

   # スマッシュ攻撃
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS smash_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       usmash_x FLOAT,
       usmash_y FLOAT,
       usmash_damage INTEGER,
       usmash_startup INTEGER,
       usmash_weapon FLOAT,
       dsmash_x FLOAT,
       dsmash_y FLOAT,
       dsmash_damage INTEGER,
       dsmash_startup INTEGER,
       dsmash_weapon FLOAT,
       fsmash_x FLOAT,
       fsmash_y FLOAT,
       fsmash_damage INTEGER,
       fsmash_startup INTEGER,
       fsmash_weapon FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')

   # つかみ
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS throw_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       x FLOAT,
       y FLOAT,
       damage INTEGER,
       startup INTEGER,
       weapon FLOAT,
       d_x FLOAT,
       d_y FLOAT,
       d_damage INTEGER,
       d_startup INTEGER,
       d_weapon FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')

   # ダッシュ攻撃
   cursor.execute('''
   CREATE TABLE IF NOT EXISTS dash_moves (
       id INTEGER PRIMARY KEY,
       character_id INTEGER,
       x FLOAT,
       y FLOAT,
       damage INTEGER,
       startup INTEGER,
       weapon FLOAT,
       FOREIGN KEY (character_id) REFERENCES characters (id)
   )''')
   
   conn.commit()
   conn.close()

if __name__ == "__main__":
   create_smash_db()
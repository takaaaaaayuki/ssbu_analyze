import sqlite3

def insert_mario_data():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   # キャラクターデータの挿入
   cursor.execute('''
   INSERT INTO characters (id, name, size_x, size_y, weight)
   VALUES (1, 'Mario', 8, 14, 98)
   ''')
   
   conn.commit()
   conn.close()

def insert_B_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO B_moves (
       character_id,
       up_b_x, up_b_y, up_b_damage, up_b_startup, up_b_weapon, up_b_tobi,
       side_b_x, side_b_y, side_b_damage, side_b_startup, side_b_weapon, side_b_tobi,
       down_b_x, down_b_y, down_b_damage, down_b_startup, down_b_weapon, down_b_tobi,
       neutral_b_x, neutral_b_y, neutral_b_damage, neutral_b_startup, neutral_b_weapon, neutral_b_tobi
   )
   VALUES (
       1,
       16, 51, 11, 3, 0, 0,
       11, 11, 7, 12, 1, 0,
       100, 55, 0, 3, 1, 0,
       90, 12, 5, 21, 0, 0
   )
   ''')
   
   conn.commit()
   conn.close()

def insert_tilt_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO kyou_zyaku_moves (
       character_id,
       utilt_startup, utilt_damage, utilt_x, utilt_y, utilt_weapon,
       ftilt_startup, ftilt_damage, ftilt_x, ftilt_y, ftilt_weapon,
       dtilt_startup, dtilt_damage, dtilt_x, dtilt_y, dtilt_weapon,
       jab_startup, jab_damage, jab_x, jab_y, jab_weapon
   )
   VALUES (
       1,
       5, 6.6, 5, 10, 0,
       5, 8.4, 10, 5, 0,
       5, 8.4, 100, 55, 0,
       2, 9.4, 9, 3, 0
   )
   ''')
   
   conn.commit()
   conn.close()

def insert_smash_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO smash_moves (
       character_id,
       usmash_startup, usmash_damage, usmash_x, usmash_y, usmash_weapon,
       fsmash_startup, fsmash_damage, fsmash_x, fsmash_y, fsmash_weapon,
       dsmash_startup, dsmash_damage, dsmash_x, dsmash_y, dsmash_weapon
   )
   VALUES (
       1,
       5, 16.8, 20, 15, 0,
       15, 12, 12, 9, 0,
       9, 17.6, 20, 5, 0
   )
   ''')
   
   conn.commit()
   conn.close()

def insert_air_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO air_moves (
       character_id,
       uair_startup, uair_damage, uair_x, uair_y, uair_weapon,
       fair_startup, fair_damage, fair_x, fair_y, fair_weapon,
       dair_startup, dair_damage, dair_x, dair_y, dair_weapon,
       bair_startup, bair_damage, bair_x, bair_y, bair_weapon,
       nair_startup, nair_damage, nair_x, nair_y, nair_weapon
   )
   VALUES (
       1,
       4, 8.4, 21, 11, 0,
       16, 16.8, 6, 14, 0,
       5, 9.8, 17, 17, 0,
       23, 12.6, 15, 7, 0,
       3, 8.1, 11, 8, 0
   )
   ''')
   
   conn.commit()
   conn.close()

def insert_dash_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO dash_moves (
       character_id,
       startup, damage, x, y, weapon
   )
   VALUES (
       1,
       6, 9.6, 18, 4, 0
   )
   ''')
   
   conn.commit()
   conn.close()

def insert_throw_moves():
   conn = sqlite3.connect('smash_characters.db')
   cursor = conn.cursor()
   
   cursor.execute('''
   INSERT INTO throw_moves (
       character_id,
       startup, damage, x, y, weapon,
       d_startup, d_damage, d_x, d_y, d_weapon
   )
   VALUES (
       1,
       6, 0, 8, 5, 0,
       9, 0, 11, 5, 0
   )
   ''')
   
   conn.commit()
   conn.close()

if __name__ == "__main__":
   insert_mario_data()
   insert_B_moves()
   insert_tilt_moves()
   insert_smash_moves()
   insert_air_moves()
   insert_dash_moves()
   insert_throw_moves()
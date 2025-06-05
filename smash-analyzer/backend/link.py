import sqlite3

def insert_link_data():
    conn = sqlite3.connect('smash_characters.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO characters (id, name, size_x, size_y, weight)
    VALUES (2, 'Link', 5, 20, 104)
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
        2,
        32, 15, 16.8, 7, 1, 0,
        110, 7, 9.6, 27, 0, 1,
        50, 50, 8.4, 12, 0, 0,
        265, 4, 6, 16, 0, 1
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
        jab_damage, jab_startup, jab_weapon, jab_x, jab_y,
        ftilt_damage, ftilt_startup, ftilt_weapon, ftilt_x, ftilt_y,
        utilt_damage, utilt_startup, utilt_weapon, utilt_x, utilt_y,
        dtilt_damage, dtilt_startup, dtilt_weapon, dtilt_x, dtilt_y
    )
    VALUES (
        2,
        12, 8, 1, 13, 11,
        15.6, 15, 1, 14, 16,
        13.2, 8, 1, 2, 14,
        10.8, 10, 1, 18, 1
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
        fsmash_damage, fsmash_startup, fsmash_weapon, fsmash_x, fsmash_y,
        usmash_damage, usmash_startup, usmash_weapon, usmash_x, usmash_y,
        dsmash_damage, dsmash_startup, dsmash_weapon, dsmash_x, dsmash_y
    )
    VALUES (
        2,
        8.4, 17, 1, 20, 6,
        4.8, 10, 1, 5, 18,
        16.8, 12, 1, 37, 4
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
        nair_damage, nair_startup, nair_weapon, nair_x, nair_y,
        fair_damage, fair_startup, fair_weapon, fair_x, fair_y,
        bair_damage, bair_startup, bair_weapon, bair_x, bair_y,
        uair_damage, uair_startup, uair_weapon, uair_x, uair_y,
        dair_damage, dair_startup, dair_weapon, dair_x, dair_y
    )
    VALUES (
        2,
        13.2, 7, 1, 7, 2,
        9.6, 16, 1, 15, 4,
        6, 6, 1, 7, 5,
        18, 11, 1, 2, 14,
        21.6, 14, 1, 14, 3
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
        damage, startup, weapon, x, y
    )
    VALUES (
        2,
        0, 9, 0, 10, 2
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
        damage, startup, weapon, x, y,
        d_damage, d_startup, d_weapon, d_x, d_y
    )
    VALUES (
        2,
        0, 6, 0, 5, 2,
        0, 9, 0, 10, 2
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_link_data()
    insert_B_moves()
    insert_tilt_moves()
    insert_smash_moves()
    insert_air_moves()
    insert_dash_moves()
    insert_throw_moves()
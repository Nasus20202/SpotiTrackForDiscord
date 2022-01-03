import sqlite3
from sqlite3 import Error

db_file = "songs.db"


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn

def new_song(song_id, plays = 0, db = create_connection()):
    if(check_if_exists(song_id, db)):
        return
    sql = ''' INSERT INTO songs(id,plays)VALUES(?,?) '''
    try:
        cur = db.cursor()
        cur.execute(sql, [song_id, plays])
        db.commit()
        return cur.lastrowid
    except Error as e:
        print(e)

def get_song_plays(song_id, db = create_connection()):
    if(not check_if_exists(song_id, db)):
        return 0
    sql = ' SELECT plays FROM songs WHERE id = "' + song_id + '" '
    try:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchall()[0][0]
    except Error as e:
        print(e)

def update_song(song_id, plays = 0, db = create_connection()):
    if(not check_if_exists(song_id, db)):
        new_song(song_id, plays, db)
        return
    sql = ' UPDATE songs SET plays = "' + str(plays) + '" WHERE id = "' + song_id + '" '
    try:
        cur = db.cursor()
        cur.execute(sql)
        db.commit()
        return cur.lastrowid
    except Error as e:
        print(e)
    

def create_tables(db = create_connection()):
    sql_create_tables = """ CREATE TABLE IF NOT EXISTS songs (
                            id TEXT PRIMARY KEY,
                            plays INTEGER
    ); """
    try:
        c = db.cursor()
        c.execute(sql_create_tables)
    except Error as e:
        print(e)

def check_if_exists(song_id, db = create_connection()):
    sql = 'SELECT EXISTS(SELECT 1 FROM songs WHERE id="' + song_id + '");'
    try:
        c = db.cursor()
        c.execute(sql)
        i = c.fetchall()[0][0]
        if(i > 0):
            return True
        return False
    except Error as e:
        print(e)

def get_top_song(count = 10, db = create_connection()):
    sql = 'SELECT * FROM songs ORDER BY plays DESC LIMIT ' + str(count)
    try:
        cur = db.cursor()
        cur.execute(sql)
        return cur.fetchall()
    except Error as e:
        print(e)


def new_record(song_id, db = create_connection()):
    update_song(song_id, get_song_plays(song_id, db) + 1, db)

create_tables()
import sys
# TODO: fix appending to path variable
sys.path.append('./')
import os
from src.services.db import db

# TODO: fix hardcoded path
BASE_PATH = './src/services/db/storage'
DATABASE = 'music.db'

class ImportData:
    def __init__(self, database, logger=print):
        self.db = database
        self.log = logger

    def initializeTable(self):
        query = """
            CREATE TABLE IF NOT EXISTS genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS album (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS album_genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                album_id INTEGER,
                genre_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS album_artist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                album_id INTEGER,
                artist_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS artist_genre (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre_id INTEGER,
                artist_id INTEGER
            );

            CREATE TABLE IF NOT EXISTS pitchfork_review (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reviewed_at INTEGER,
                album_id INTEGER,
                link TEXT,
                tag TEXT
            );

            CREATE TABLE IF NOT EXISTS pitchfork_author (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS pitchfork_review_pitchfork_author (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pitchfork_review_id INT,
                pitchfork_author_id INT
            );
            """
        result = self.db.writeScript(query)

if __name__ == '__main__':
    if not os.path.exists(BASE_PATH):
        os.makedirs(BASE_PATH)
    
    db = db.__BaseDatabase()
    db.connect(os.path.join(BASE_PATH, DATABASE))
    
    dataHandler = ImportData(db)
    dataHandler.initializeTable()

    db.closeConnection()
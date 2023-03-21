from customtypes import Album, Artist, Review
from services.db.db import __BaseDatabase
from services.db.models.artist import Artist
import logging
import os

class AlbumModel(__BaseDatabase):
    # TODO: remove hardcoded path
    DATABASE_NAME = './src/services/db/storage/music.db'

    def __init__(self):
        logger = logging.getLogger(__name__)
        super(AlbumModel, self).__init__(logger)
        self.connect(self.DATABASE_NAME)
        self.connection.row_factory = self.__rowFactory

    def __rowFactory(self, cursor, row):
        print(row)
        return Album(
            artists=[Artist(genres=row[7].split(','), name=name) for name in row[6].split(',')],
            name=row[0],
            genres=row[1].split(','),
            review=Review(
                author=row[5],
                link=row[3],
                reviewedAt=row[2],
                tag=row[4]
            )
        )

    def getByName(self, name):            
        query = """
            with data AS (
                SELECT 
                    album.name as album_name,
                    genre.name as genre,
                    reviewed_at,
                    link,
                    tag,
                    pitchfork_author.name as author,
                    artist.name as artists,
                    artist.id as artist_id
                FROM album
                JOIN album_genre ON album_genre.album_id=album.id 
                JOIN genre ON genre.id=album_genre.genre_id
                JOIN pitchfork_review ON pitchfork_review.album_id=album.id
                JOIN pitchfork_review_pitchfork_author ON pitchfork_review.id = pitchfork_review_pitchfork_author.pitchfork_review_id
                JOIN pitchfork_author ON pitchfork_author.id = pitchfork_review_pitchfork_author.pitchfork_author_id
                JOIN album_artist ON album.id=album_artist.album_id
                JOIN artist ON artist.id=album_artist.artist_id
                WHERE album.name = (?))
            SELECT 
                DISTINCT album_name, 
                group_concat(genre) as genres,
                reviewed_at,
                link,
                tag,
                author,
                group_concat(artists) as artists,
                group_concat(genre.name) as artist_genres
            FROM data
            JOIN artist_genre ON data.artist_id=artist_genre.artist_id
            JOIN genre ON artist_genre.genre_id=genre.id"""
        return self.read(query, (name, ))[0]

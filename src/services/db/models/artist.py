from customtypes import Artist, Album, Review
from services.db.db import __BaseDatabase
import logging
import os

class ArtistModel(__BaseDatabase):
    # TODO: remove hardcoded path
    DATABASE_NAME = './src/services/db/storage/music.db'

    def __init__(self):
        logger = logging.getLogger(__name__)
        super(ArtistModel, self).__init__(logger)
        self.connect(self.DATABASE_NAME)
        self.connection.row_factory = self.__rowFactory

    def __rowFactory(self, cursor, row):
        print(row)
        return Artist(
            albums=[Album(name=name, genres=row[7].split(','), review=Review(author=row[5], link=[3], reviewedAt=row[2], tag=row[4])) for name in row[6].split(',')],
            name=row[0],
            genres=row[1].split(','),
        )

    def getByName(self, name):
        query = """
            with data AS (
                SELECT 
                    artist.name as artist_name,
                    genre.name as genre,
                    reviewed_at,
                    link,
                    tag,
                    pitchfork_author.name as author,
                    album.name as albums,
                    album.id as album_id
                FROM artist
                JOIN artist_genre ON artist_genre.artist_id=artist.id 
                JOIN genre ON genre.id=artist_genre.genre_id
                JOIN album_artist ON artist.id=album_artist.artist_id
                JOIN album ON album.id=album_artist.album_id
                JOIN pitchfork_review ON pitchfork_review.album_id=album.id
                JOIN pitchfork_review_pitchfork_author ON pitchfork_review.id = pitchfork_review_pitchfork_author.pitchfork_review_id
                JOIN pitchfork_author ON pitchfork_author.id = pitchfork_review_pitchfork_author.pitchfork_author_id
                WHERE artist.name = (?))
            SELECT 
                group_concat(artist_name), 
                group_concat(genre) as genres,
                reviewed_at,
                link,
                tag,
                author,
                group_concat(albums) as albums,
                group_concat(genre.name) as album_genres
            FROM data
            JOIN album_genre ON data.album_id=album_genre.album_id
            JOIN genre ON album_genre.genre_id=genre.id"""
        result = self.read(query, (name, ))
        return result[0]
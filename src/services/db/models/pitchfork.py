from customtypes import PitchforkReview
from db.db import __BaseDatabase
import logging
import os

class PitchForkReviewModel(__BaseDatabase):
    # TODO: remove hardcoded path
    DATABASE_NAME = './services/db/storage/music.db'

    def __init__(self):
        logger = logging.getLogger(__name__)
        super(PitchForkReviewModel, self).__init__(logger)
        self.connect(self.DATABASE_NAME)

    def _saveAlbum(self, album) -> int :
        query = """SELECT id FROM album WHERE name = (?)"""
        album_id = self.read(query, (album, ))
        if len(album_id) == 0:
            query = """INSERT INTO album (name) VALUES (?)"""
            album_id = self.write(query, (album, )).lastrowid
        else:
            album_id = album_id[0][0]
        return album_id

    def _saveAlbumGenreAssociation(self, albumId: int, genreIds: [int]) -> None:
        for genreId in genreIds:
            query = """INSERT INTO album_genre (album_id, genre_id) VALUES (?, ?)"""
            self.write(query, (albumId, genreId, ))

    def _saveAlbumArtistAssociation(self, albumId: int, artistIds: [int]) -> None:
        for artistId in artistIds:
            query = """INSERT INTO album_artist (album_id, artist_id) VALUES (?, ?)"""
            self.write(query, (albumId, artistId, ))
    
    def _saveArtists(self, artists: [str]) -> [int]:
        result = []
        for artist in artists:
            query = """SELECT id FROM artist WHERE name = (?)"""
            artist_id = self.read(query, (artist, ))       
            if len(artist_id) == 0:
                query = """INSERT INTO artist (name) VALUES (?)"""
                artist_id = self.write(query, (artist, )).lastrowid
                result.append(artist_id)
            else:
                result.append(artist_id[0][0])
        return result

    def _saveArtistGenreAssociation(self, artistIds: [int], genreIds: [int]) -> None:
        for artistId in artistIds:
            for genreId in genreIds:
                query = """INSERT INTO artist_genre (artist_id, genre_id) VALUES (?, ?)"""
                self.write(query, (artistId, genreId, ))
    
    def _saveGenres(self, genres) -> [int] :
        result = []
        for genre in genres:
            query = """SELECT id FROM genre WHERE name = (?)"""
            genre_id = self.read(query, (genre, ))
            if len(genre_id) == 0:
                query = """INSERT INTO genre (name) VALUES (?)"""
                genre_id = self.write(query, (genre,)).lastrowid
                result.append(genre_id)
            else:
                genre_id = genre_id[0][0]
                result.append(genre_id)
        return result

    def _savePitchforkReview(self, albumId: str, link: str, reviewedAt: str, tag) -> int:
        query = """INSERT INTO pitchfork_review (reviewed_at, album_id, link, tag) VALUES (?, ?, ?, ?)"""
        pitchfork_review_id = self.write(query, (reviewedAt, albumId, link, tag)).lastrowid
        return pitchfork_review_id

    def _saveReviewAuthor(self, author: str) -> int:
        query = """SELECT id FROM pitchfork_author WHERE name = (?)"""
        review_author_id = self.read(query, (author, ))
        if len(review_author_id) == 0:
            query = """INSERT INTO pitchfork_author (name) VALUES (?)"""
            review_author_id = self.write(query, (author, )).lastrowid
        else:
            review_author_id = review_author_id[0][0]
        return review_author_id

    def _saveReviewAuthorAssociation(self, authorId: int, reviewId: str) -> None:
        query = """INSERT INTO pitchfork_review_pitchfork_author (pitchfork_review_id, pitchfork_author_id) VALUES (?, ?)"""
        self.write(query, (reviewId, authorId,))
    
    def load(self, item: PitchforkReview) -> None:
        self.album = item.album
        self.artists = item.artists
        self.author = item.meta['author']
        self.genres = item.genres
        self.link = item.link
        self.reviewedAt = item.meta['reviewed_at']
        self.tags = item.meta['tag']

    def save(self) -> None:
        # TODO: wrap these in a transaction - all should succeed or rollback to avoid data inconsistency
        albumId = self._saveAlbum(self.album)
        genreIds = self._saveGenres(self.genres)
        self._saveAlbumGenreAssociation(albumId, genreIds)

        artistIds = self._saveArtists(self.artists)
        self._saveAlbumArtistAssociation(albumId, artistIds)
        self._saveArtistGenreAssociation(artistIds, genreIds)

        reviewAuthorId = self._saveReviewAuthor(self.author)
        reviewId = self._savePitchforkReview(albumId, self.link, self.reviewedAt, self.tags)

        self._saveReviewAuthorAssociation(reviewAuthorId, reviewId)
import typing
import strawberry
from db.models.album import AlbumModel
from db.models.artist import ArtistModel
from typing import Optional, Annotated
from dataclasses import dataclass


@strawberry.type
class ArtistType:
    albums: typing.List[Annotated['AlbumType', 'AlbumType']]
    genres: typing.List[str]
    name: str

@strawberry.type
class ReviewType:
    author: str
    link: str
    reviewedAt: str
    tag: Optional[str]

@strawberry.type
class AlbumType:
    artists: typing.List[ArtistType]
    genres: typing.List[str]
    name: str
    review: ReviewType

@strawberry.type
class Query:
    @strawberry.field
    def artist(self, name: str) -> ArtistType:
        return ArtistModel().getByName(name)

    @strawberry.field
    def album(self, name: str) -> AlbumType:
        return AlbumModel().getByName(name)

schema = strawberry.Schema(query=Query)
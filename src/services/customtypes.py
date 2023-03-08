from dataclasses import dataclass
import typing

@dataclass
class PitchforkReview:
    """Dataclass for storing state of a scraped review from Pitchfork"""
    album: str
    artists: typing.List[str]
    genres: typing.List[str]
    link: str
    """
    Key values for meta object
    {
        author: str,
        reviewed_at: datetime.datetime,
        tags: typing.List[str]
    }
    TODO: flatten out meta object
    """
    meta: typing.Dict[str, str]
from pydantic import BaseModel


class AvailableArtists(BaseModel):
    available_artists: list[str]


class SimilarArtists(BaseModel):
    similar_artists: list[str]

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from . import models


def get_available_artists(
    db: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[models.Artist]:
    """
    Retrieves names of artists that occured in dataset.
    """
    query = select(models.Artist).offset(offset).limit(limit)
    return db.execute(query).scalars().all()


def get_artist(
    db: Session,
    name: str,
) -> models.Artist | None:
    """
    Searching for the artist with the given name ignoring it's case.
    """
    query = select(models.Artist).where(models.Artist.name.ilike(name)).limit(1)
    return db.execute(query).scalars().first()


def get_similar_artists(
    db: Session, artist: models.Artist, limit: int = 5,
) -> list[models.Artist] | None:
    """
    Returns a list of similar artists.
    """
    associated_playlist_ids = (
        db.execute(
            select(models.Playlist.id)
            .join(models.Playlist.tracks)
            .join(models.Track.artist)
            .filter(models.Artist.name == artist.name)
        )
        .scalars()
        .all()
    )

    return (
        db.execute(
            select(models.Artist)
            .join(models.Artist.tracks)
            .filter(models.Artist.name != artist.name)
            .join(models.Track.playlists)
            .filter(models.Playlist.id.in_(associated_playlist_ids))
            .group_by(models.Artist.name)
            .order_by(func.count(models.Artist.name).desc())
            .limit(5)
        )
        .scalars()
        .all()
    )

from sqlalchemy import select, func

from . import models
from .database import Session


def get_available_artists(
    db: Session,
    offset: int = 0,
    limit: int = 100,
) -> list[str]:
    """
    Retrieves names of artists that occured in dataset.
    """
    query = select(models.Artist.name).offset(offset).limit(limit)

    return db.execute(query).scalars().all()


def get_similar_artists(
    db: Session,
    artist_name: str,
) -> list[str]:
    associated_playlist_ids = (
        db.execute(
            select(models.Playlist.id)
            .join(models.Playlist.tracks)
            .join(models.Track.artist)
            .filter(models.Artist.name == artist_name)
        )
        .scalars()
        .all()
    )

    result = (
        db.execute(
            select(models.Artist.name)
            .join(models.Artist.tracks)
            .filter(models.Artist.name != artist_name)
            .join(models.Track.playlists)
            .filter(models.Playlist.id.in_(associated_playlist_ids))
            .group_by(models.Artist.name)
            .order_by(func.count(models.Artist.name).desc())
            .limit(5)
        )
        .scalars()
        .all()
    )

    return result

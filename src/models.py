from __future__ import annotations

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Edge(Base):

    __tablename__ = "edges"

    track_id = Column(String, ForeignKey("tracks.id"), primary_key=True)
    playlist_id = Column(Integer, ForeignKey("playlists.id"), primary_key=True)


class Playlist(Base):

    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    tracks: list[Track] = relationship(
        "Track", secondary=Edge.__table__, back_populates="playlists"
    )

    def __repr__(self):
        return f"<Playlist name={self.name}>"


class Artist(Base):

    __tablename__ = "artists"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    tracks: list["Track"] = relationship("Track", back_populates="artist")

    def __repr__(self):
        return f"<Artist name={self.name}>"


class Track(Base):

    __tablename__ = "tracks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    artist_id = Column(String, ForeignKey("artists.id"), nullable=False)

    artist: Artist = relationship("Artist", back_populates="tracks")

    playlists: list["Playlist"] = relationship(
        "Playlist", secondary=Edge.__table__, back_populates="tracks"
    )

    def __repr__(self):
        return f"Track<name={self.name}>"

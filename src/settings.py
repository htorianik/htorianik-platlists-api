from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    sa_database_uri = "sqlite:///data/playlists_1000.sqlite"


@lru_cache()
def get_settings() -> Settings:
    return Settings()

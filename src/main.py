from fastapi import FastAPI, Depends

from . import models, schemas, crud
from .database import Session, engine
from .settings import get_settings


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


settings = get_settings()


# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.get("/similar_artists/{artist_name}", response_model=schemas.SimilarArtists)
def get_similar_artists(
    artist_name: str,
    db: Session = Depends(get_db),
):
    return {"similar_artists": crud.get_similar_artists(db, artist_name)}


@app.get("/available_artists", response_model=schemas.AvailableArtists)
def available_artists(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return {"available_artists": crud.get_available_artists(db, offset, limit)}

from typing import Generator

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas, crud
from .database import SessionFactory, engine
from .settings import get_settings


models.Base.metadata.create_all(bind=engine)


app = FastAPI()


settings = get_settings()


# Dependency
def get_db() -> Generator[Session, None, None]:
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()


@app.post("/similar_artists", response_model=list[schemas.Artist])
def similar_artists(
    input_artist: schemas.Artist,
    db: Session = Depends(get_db),
):
    print("Hello world")
    if artist := crud.get_artist(db, input_artist.name):
        return crud.get_similar_artists(db, artist)
    raise HTTPException(status_code=404, detail="Artist not found")


@app.post("/available_artists", response_model=list[schemas.Artist])
def available_artists(
    pagination: schemas.PaginationConfig, db: Session = Depends(get_db)
):
    return crud.get_available_artists(db, pagination.offset, pagination.limit)

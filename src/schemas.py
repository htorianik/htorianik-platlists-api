from pydantic import BaseModel


class Artist(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PaginationConfig(BaseModel):
    offset: int = 0
    limit: int = 100

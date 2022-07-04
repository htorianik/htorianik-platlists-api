from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from .settings import get_settings


settings = get_settings()

engine = create_engine(settings.sa_database_uri)

Session = sessionmaker(bind=engine)

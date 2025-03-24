import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

Base = declarative_base()

DATABASE_URL = "postgresql+psycopg2://postgres:user@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

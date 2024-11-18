from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_PATH = f'postgresql+psycopg2://avnadmin:{os.environ.get('password')}@challenge-challenge-globant-3b2c.k.aivencloud.com:25318/challenge?sslmode=require'

engine = create_engine(
    SQLALCHEMY_DATABASE_PATH,
)

localsession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

def get_db():
    db = localsession()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()

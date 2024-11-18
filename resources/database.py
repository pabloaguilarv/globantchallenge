from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_PATH = 'postgresql://postgres:Sez7dllxPA@localhost:5432/challenge'
SQLALCHEMY_DATABASE_PATH = 'postgresql+psycopg2://avnadmin:AVNS_9V67I1GWUPLcMF93Bhh@challenge-challenge-globant-3b2c.k.aivencloud.com:25318/challenge?sslmode=require'

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

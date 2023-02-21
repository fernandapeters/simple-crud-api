from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:psswrd@db:5432"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

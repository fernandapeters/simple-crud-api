from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:psswrd@db:5432"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

LocalSession = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

#GLOBAL VARIABLES#
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST","db")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","5432")

CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(CONNECTION_STRING)
session_local = sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base = declarative_base()

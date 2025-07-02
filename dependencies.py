from fastapi import Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
import os

load_dotenv()

def get_redis(request: Request):
    return request.app.state.redis

eventurl = os.getenv("EURL")

engine = create_engine(eventurl)

sessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_inj = Annotated[Session, Depends(get_db)]
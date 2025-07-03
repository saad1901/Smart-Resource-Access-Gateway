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
hotelurl = os.getenv("HURL")

engine = create_engine(eventurl)
engine2 = create_engine(eventurl)

sessionLocal = sessionmaker(autoflush=True, autocommit=False, bind=engine)
sessionLocal2 = sessionmaker(autoflush=True, autocommit=False, bind=engine2)

Base = declarative_base()
Base2 = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db2():
    db = sessionLocal2()
    try:
        yield db
    finally:
        db.close()

db_inj = Annotated[Session, Depends(get_db)]
db_inj2 = Annotated[Session, Depends(get_db2)]
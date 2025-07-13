from fastapi import APIRouter, HTTPException
from starlette import status
from config.dependencies import db_inj
from jose import jwt
from models.Emodels import BlackJWT
from config.authentication import secret

router = APIRouter()

@router.post('/blockToken',name='BlackList Token')
async def blockjwt(tokenOld: str, db: db_inj):
    try:
        jwt.decode(tokenOld,secret)
    except:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Inavalid Token")
    
    token = BlackJWT(
        token = tokenOld.split('.')[-1]
    )

    db.add(token)
    db.commit()

    return {"detail": 'TOken BLocked SUccesfully'}
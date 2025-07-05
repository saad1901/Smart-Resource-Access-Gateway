from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from config.dependencies import db_inj, get_redis
from models.Emodels import Upis, Participant, Tournament, User
from structure.pdmodel import UpiInBody, UserIn
import json
from config.authentication import verifyUsers

router = APIRouter()
# , redis = Depends(get_redis)

@router.post('/authuser')
async def verifyUser(db: db_inj, req: UserIn):
    if req.username and req.passwword:
        token = verifyUsers(db, req.username, req.passwword)

        if not token:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= 'User Not Authenticated')

        return { "Token Bearer" : token, 'Token Type' : "jwt"}
    

@router.get('/')
async def getuser(db: db_inj):
    user = db.query(User).all()

    return user

# @router.get('/')
# async def upi_ids(db : db_inj):

#     print("Not Found in Redis")
#     upis = db.query(Upis).all()
#     upis_list = [
#         {
#             "id": u.id,
#             "name": u.name,
#             "nickname": u.nickname,
#             "upi_id": u.upi_id,
#         } for u in upis
#     ]
#     if upis:
#         # redis.set('users:all',json.dumps(upis_list))
#         return upis_list
    
#     return 'No UPI IDs Found'

# @router.post('/addupi')
# async def addupi(db: db_inj, req: UpiInBody):
#     new_id = Upis(
#         name = req.name,
#         upi_id = req.upi_id,
#         nickname = req.nickname
#     )
#     db.add(new_id)
#     db.commit()

#     return {'Success'}

# @router.get('/participants')
# async def getparts(db: db_inj):
#     participants = db.query(Participant).all()

#     if participants:
#         return participants
    
#     else: return {"No Participant Data Found"}

# @router.get('/events')
# async def getevents(db: db_inj):
#     events = db.query(Tournament).all()

#     if events:
#         return events
    
#     else: return {"No Events Data Found"}
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from config.dependencies import db_inj, get_redis
from models.Emodels import Upis, Participant, Tournament, User
from structure.pdmodel import UpiInBody, UserAdd, UserIn
from config.authentication import verifyUsers, verifyToken, crypto
from fastapi.security import OAuth2PasswordBearer
import json

router = APIRouter()
# , redis = Depends(get_redis)

# @router.post('/verifyToken')

bearer = OAuth2PasswordBearer(tokenUrl='/login')

@router.post('/login')
async def Login(db: db_inj, req: UserIn):
    if req.username and req.password:
        token = verifyUsers(db, req.username, req.password)
        
        if not token:
            raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= 'User Not Authenticated')

        return { "Token" : f'Bearer {token}', 'Token Type' : "access/jwt"}
    
@router.get('/getuser')
async def getuser(db: db_inj, token: str = Depends(bearer)):
    payload = verifyToken(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user = db.query(User).filter(User.id == payload['id']).first()
    return user

@router.post('/adduser')
async def adduser(user : UserAdd, db: db_inj, token: str = Depends(bearer)):
    payload = verifyToken(token)
    if payload.get('superuser'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Non SuperUsers Are not Allowed to Perfom This Action")
    
    user = User(
        username = user.username,
        email = user.email,
        password = crypto.hash(user.password)
    )

    db.add(user)
    db.commit()

    return {'User Added Succesfully'}

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
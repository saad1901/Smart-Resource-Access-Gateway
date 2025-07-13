from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from typing import List
from config.dependencies import db_inj, get_redis
from models.Emodels import Upis, Participant, Tournament, User, EventData
from structure.Event import OrgIn, UpiInBody, UserAdd, UserIn, EventIn, EventOut, OrgOut, ParticipantOut, UpiOutBody
from config.authentication import verifyUsers, verifyToken, crypto
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import json

router = APIRouter()
# , redis = Depends(get_redis)

bearer = OAuth2PasswordBearer(tokenUrl='/events/login/')

@router.post('/login')
async def Login(db: db_inj, req: UserIn):
    if req.username and req.password:
        token = verifyUsers(db, req.username, req.password)

        return { "Token" : f'Bearer {token}', 'Token Type' : "access/jwt"}
    
@router.get('/getuser')
async def getuser(db: db_inj, token: str = Depends(bearer)):
    payload = verifyToken(db,token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    
    user = db.query(User).filter(User.id == payload['id']).first()
    return user

@router.get('/getalluser')
async def getalluser(db: db_inj):

    
    user = db.query(User).all()
    return user
    
@router.post('/adduser')
async def adduser(user : UserAdd, db: db_inj, token: str = Depends(bearer)):
    payload = verifyToken(db,token)
    if not payload.get('superuser'):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you Are not Allowed to Perfom This Action")
    
    user = User(
        username = user.username,
        first_name = user.first_name,
        last_name = user.last_name,
        email = user.email,
        password = crypto.hash(user.password)
    )

    db.add(user)
    db.commit()

    return {'User Added Succesfully'}

@router.get('/events', response_model=List[EventOut], name='Get All Events')
async def getevents(db: db_inj, token: str = Depends(bearer)):
    user = verifyToken(db,token)
    
    events = db.query(Tournament).all()

    if events:
        return events
    
    else: return {"No Events Data Found"}

@router.post('/addevent', name='Add Event')
async def addevent(db: db_inj, event: EventIn):
    event = Tournament(**event.model_dump())

    db.add(event)
    # try:
    db.commit()

    # except:
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail='missing or mismatched column names')

@router.get('/orginfo', name='Organization Info', response_model=OrgOut)
async def orginfo(db: db_inj):
    org = db.query(EventData).first()

    return org

@router.put('/orginfo', name='Update Organization Info', status_code=status.HTTP_202_ACCEPTED)
async def inorginfo(db: db_inj, req: OrgIn):
    org = db.query(EventData).first()
    org.name = req.name
    org.add = req.add
    org.wp = req.wp
    org.email = req.email
    try:
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='SomeFields Mismatches DataType / Null')
    return {"Details Updated Sucessfully"}

@router.get('/participants', response_model=List[ParticipantOut])
async def getparts(db: db_inj):
    participants = db.query(Participant).all()

    if participants:
        return participants
    
    else: return {"No Participant Data Found"}

@router.get('/getupi', response_model=List[UpiOutBody])
async def upi_ids(db : db_inj):

    upis = db.query(Upis).all()
    if upis:

        return upis
    
    return 'No UPI IDs Found'

@router.post('/addupi')
async def addupi(db: db_inj, req: UpiInBody):
    new_id = Upis(
        name = req.name,
        upi_id = req.upi_id,
        nickname = req.nickname
    )
    db.add(new_id)
    db.commit()

    return {'Success'}

@router.put('/updateupi' , status_code=status.HTTP_202_ACCEPTED)
async def updateupi(db: db_inj, req: UpiOutBody):
    upi = db.query(Upis).filter(Upis.id == req.id).first()
    if not upi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"UPI ID of Id = {req.id} Not Found")
    
    upi.name = req.name
    upi.upi_id = req.upi_id
    upi.nickname = req.nickname
    
    try:
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='SomeFields Mismatches DataType / Null')   
    
    return {"details" : "UPI ID updated Successfully"}

@router.delete('/deleteupi', status_code=status.HTTP_204_NO_CONTENT)
async def deleteupi(db: db_inj, id: int):
    upi = db.query(Upis).filter(Upis.id == id).first()

    if not upi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"UPI ID of Id = {id} Not Found")
    
    try:
        db.delete(upi)
        db.commit()
    except:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Database Rejected The Action")
    
    return {"details" : "UPI ID deleted Successfully"}
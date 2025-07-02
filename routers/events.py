from fastapi import APIRouter, Depends
from dependencies import db_inj
from models import Upis, Participant, Tournament
from pdmodel import UpiInBody

router = APIRouter()

@router.get('/')
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

@router.get('/participants')
async def getparts(db: db_inj):
    participants = db.query(Participant).all()

    if participants:
        return participants
    
    else: return {"No Participant Data Found"}

@router.get('/events')
async def getevents(db: db_inj):
    events = db.query(Tournament).all()

    if events:
        return events
    
    else: return {"No Events Data Found"}
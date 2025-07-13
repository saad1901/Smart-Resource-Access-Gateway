from fastapi import APIRouter, Depends
from models.Hmodels import User
from structure.Hotel import UserIn
from config.dependencies import db_inj2

router = APIRouter()


@router.post('/adduser')
async def adduser(r: UserIn, db: db_inj2):
    user = User(
        username = r.username,
        password = r.password,
        email = r.email,
        first_name = r.first_name,
        last_name = r.last_name,
        is_active = r.is_active,
        is_staff = r.is_staff,
        is_superuser = r.is_superuser
    )

    db.add(user)
    db.commit()

@router.get('/getusers')
async def getusers(db: db_inj2):
    users = db.query(User).all()

    if users: return users

    return "No users in database"
from fastapi import HTTPException
from starlette import status
from models.Emodels import User, BlackJWT
from passlib.context import CryptContext
from jose import jwt
import os

crypto = CryptContext(
    schemes=["django_bcrypt_sha256", "bcrypt_sha256", "bcrypt"],
    deprecated="auto"
)
secret = 'abcd1234'

def generate_token(id:int, sup: bool):
    sub = {'id' : id, 'superuser' : sup, 'salt' : os.urandom(8).hex()}
    token = jwt.encode(sub, secret, algorithm='HS256')
    print("token :", token)
    return token

def verifyUsers(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print('User not correct')
        raise HTTPException(status_code=401, detail='Invalid credentials')
    try:
        print(crypto.hash(password))
        print(user.password)
        # auth = crypto.verify(password, user.password)
        auth = crypto.verify(password, user.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if not auth:            
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    return generate_token(user.id, user.is_superuser)

def verifyToken(db,token : str):
    if token:
        if isBlocked(db, token):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token Blocked")
        try:
            payload = jwt.decode(token, secret)
            return payload
        except:
            return False
        
def isBlocked(db, token):
    token = db.query(BlackJWT).filter(BlackJWT.token == token.split('.')[-1]).first()
    if token: return True
    return False
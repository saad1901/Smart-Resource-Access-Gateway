from models.Emodels import User
from passlib.context import CryptContext
from jose import jwt

crypto = CryptContext(schemes=['bcrypt'])
secret = 'abcd1234'

def generate_token(id:int, sup: bool):
    sub = {'id' : id, 'superuser' : sup}
    token = jwt.encode(sub, secret, algorithm='HS256')
    print("token :", token)
    return token

def verifyUsers(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        print('User not correct')
        return None
    try:
        print(password)
        print(user.password)
        if crypto.verify(password, user.password):
            return generate_token(user.id, user.is_superuser)
    except:
        return None

def verifyToken(token : str):
    if token:
        try:
            payload = jwt.decode(token, secret)
            return payload
        except:
            return False
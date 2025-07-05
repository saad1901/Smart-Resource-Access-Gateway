from models.Emodels import User
from passlib.context import CryptContext
from jose import jwt

crypto = CryptContext(schemes=['bcrypt'])
secret = 'abcd1234'

def generate_token(id):
    sub = {'id' : id}
    token = jwt.encode(sub, secret, algorithm='HS256')
    print("token :", token)
    return token

def verifyUsers(db, username: str, password: str):
    hash_pass = crypto.hash(password)
    print('HASH PASSWORD ',hash_pass)
    user = db.query(User).filter(User.username == username, User.password == password).first()

    if not user:
        print('User not correct')
        return None
    
    return generate_token(user.id)


from jose import jwt
import random
from hashing import check_hash_password

secret = 'abcd1234'
hash = '$2b$12$Wwvf.rMutcPsU9SbcZ9tV.WudjsZdjLufjTvR5e044slW1yRavzgi'

sub = {'id': 1, 'username': 'saad1919', 'role' : 'admin'}
# salt = int(random.random()*1000)
# sub.update({'salt' : salt})
# print(salt)

username = input('Enter username : ')
password = input('Enter password : ')

def get_token(username: str, password: str):
    if check_hash_password(password, hash):
        return jwt.encode(sub, secret, algorithm='HS256')

    return False

try:
    token = get_token(username, password)
    if token:
        payload = jwt.decode(token, 'abcd1234')
        print("//////////SUCCESS//////////")
        print(f'TOKEN          : {token}')
        print(f'USERNAME       : {payload['username']} | ID : {payload['id']}')
    else:
        print("INVALID USER")

except Exception as e:
    print(f'ERROR : {e}')
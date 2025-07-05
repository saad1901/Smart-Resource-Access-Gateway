from passlib.context import CryptContext

crypto = CryptContext(schemes=['bcrypt'])

def get_hash_password(username : str, password : str):
    if not username or not password:
        return None

    try:    
        hashed_password = crypto.hash(password)
    except:
        return None
    
    return hashed_password

def check_hash_password(password : str , hash : str):
    if crypto.verify(password, hash):
        return True
    else: return False


# hash_pass = get_hash_password(username,password)

# if not hash_pass:
#     print("Something Went Wrong")

# else:
#     print('Hashed Password : ',hash_pass)

# checkpasss = input("Enter password again to check against the Hash : ")

# if crypto.verify(checkpasss, hash_pass):
#     print("Your Password Matched")

# else:
#     print("Password did not matched")
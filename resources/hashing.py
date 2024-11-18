from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=['bcrypt'], deprecated = 'auto')

def hash(pwd:str) -> str:
    return pwd_cxt.hash(pwd)

def verify(given_pwd:str, stored_pwd:str) -> bool:
    return pwd_cxt.verify(given_pwd, stored_pwd)
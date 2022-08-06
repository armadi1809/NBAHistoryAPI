from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.db import SessionLocal

SECRET_KEY = "13fdabf0c1e2dcf5880368952cfd7dddfb36487ba8cc5a1de638b8610328c428"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1



def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
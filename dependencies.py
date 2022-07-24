from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from db.db import SessionLocal

SECRET_KEY = "13fdabf0c1e2dcf5880368952cfd7dddfb36487ba8cc5a1de638b8610328c428"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def validate_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        b = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError: 
        raise credentials_exception
    return 1

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
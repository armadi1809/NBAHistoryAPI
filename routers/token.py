from datetime import timedelta, datetime
from typing import Union
from jose import jwt
from schemas import schemas

from fastapi import APIRouter

router = APIRouter(
    prefix = "/token", 
    tags = ["OAuth2 acces token generation"], 
)

SECRET_KEY = "13fdabf0c1e2dcf5880368952cfd7dddfb36487ba8cc5a1de638b8610328c428"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(expires_delta: Union[timedelta, None] = None):
    to_encode = {}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/", response_model=schemas.Token)
async def login_for_access_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
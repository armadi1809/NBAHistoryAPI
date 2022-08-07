from datetime import timedelta, datetime
from typing import Union
from jose import jwt
from schemas import schemas
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, Depends, status
from Auth.jwt_handler import create_access_token, authenticate_user
import os 
from dotenv import load_dotenv 
from dependencies import get_db
from sqlalchemy.orm import Session

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('EXPIRATION')

router = APIRouter(
    prefix = "/token", 
    tags = ["OAuth2 acces token generation"], 
)


# def create_access_token(expires_delta: Union[timedelta, None] = None):
#     to_encode = {}
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt

@router.post("", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
from fastapi import APIRouter, Depends, HTTPException 
from db.db import SessionLocal
from sqlalchemy.orm import Session
from schemas import schemas
from crud import crud
from typing import List
from dependencies import get_db
from Auth import jwt_handler
from models import models

router = APIRouter(
    prefix = "/user",
    tags=["User_info"]

)
@router.post("/sign-up", response_model=schemas.User)
async def signup_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)): 
    user = db.query(models.User).filter(models.User.username == user_in.username).first()
    if user:
        raise HTTPException(  # 5
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user = crud.create_user(db, user_in)
    return user

@router.get("/me", response_model = schemas.User)
async def read_my_account(current_user: schemas.User = Depends(jwt_handler.get_current_active_user)):
    return current_user
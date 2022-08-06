from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_db
from schemas import schemas
from crud import crud
from Auth import jwt_handler


router = APIRouter(
    prefix="/fact",
    tags=["Team_facts"]
)

@router.put("/{id}", response_model=schemas.Fact)
def update_fact(id: int, new_fact: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(jwt_handler.get_current_active_user)):
    if current_user.username != "armadi": 
        raise HTTPException(status_code=401, detail="This endpoint can only be accessed from an admin account")
    db_fact = crud.get_fact_by_id(db, id)
    if not db_fact: 
        return None 
    db_fact.description = new_fact
    db.commit()
    db.refresh(db_fact)
    return db_fact
    
@router.get("/random", response_model=schemas.Fact)
def get_random_fact(db: Session = Depends(get_db), current_user: schemas.User = Depends(jwt_handler.get_current_active_user)):
    return crud.get_random_fact(db)

@router.delete("/{id}")
def delete_by_id(id: int, db: Session = Depends(get_db), current_user: schemas.User = Depends(jwt_handler.get_current_active_user)) :
    if current_user.username != "armadi": 
        raise HTTPException(status_code=401, detail="This endpoint can only be accessed from an admin account")
    return crud.delete_fact_by_id(db, id)
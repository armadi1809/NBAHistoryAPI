from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from dependencies import get_db
from schemas import schemas
from crud import crud

router = APIRouter(
    prefix="/fact",
    tags=["Team_facts"]
)

@router.put("/fact/{id}", response_model=schemas.Fact)
def update_fact(id: int, new_fact: str, db: Session = Depends(get_db)):
    db_fact = crud.get_fact_by_id(db, id)
    if not db_fact: 
        return None 
    db_fact.description = new_fact
    db.commit()
    db.refresh(db_fact)
    return db_fact
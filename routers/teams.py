
from fastapi import APIRouter, Depends, HTTPException 
from db.db import SessionLocal
from sqlalchemy.orm import Session
from schemas import schemas
from crud import crud
from typing import List
from dependencies import validate_token

router = APIRouter(
    prefix = "/teams",
    tags=["NBA_Teams"]

)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@router.post("/", response_model=schemas.Team)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, name=team.name)
    if db_team: 
        raise HTTPException(status_code=400, detail="Team already registered")
    return crud.create_team(db, team=team)

@router.get("/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    db_teams = crud.get_teams(db)
    return db_teams 

@router.get("/{id}", response_model=schemas.Team)
def read_team(id: int, db: Session = Depends(get_db), valid_token: int = Depends(validate_token)):
    # validate_token(token)
    db_team = crud.get_team_by_id(db, id)
    return db_team 


@router.post("/{id}/facts", response_model=schemas.Fact)
def creat_fact_for_team(id:int, fact:schemas.FactCreate, db: Session = Depends(get_db)):
    return crud.create_team_fact(db, fact, id)


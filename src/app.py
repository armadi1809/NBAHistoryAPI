from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models, crud, schemas
app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamBase, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_name(db, name=team.name)
    if db_team: 
        raise HTTPException(status_code=400, detail="Team already registered")
    return crud.create_team(db, team=team)

@app.get("/teams/", response_model=List[schemas.Team])
def read_teams(db: Session = Depends(get_db)):
    db_teams = crud.get_teams(db)
    return db_teams 

@app.put("/fact/{id}", response_model=schemas.Fact)
def update_fact(id: int, new_fact: str, db: Session = Depends(get_db)):
    db_fact = crud.get_fact_by_id(db, id)
    if not db_fact: 
        return None 
    db_fact.description = new_fact
    db.commit()
    db.refresh(db_fact)
    return db_fact

@app.get("/teams/{id}", response_model=schemas.Team)
def read_team(id: int, db: Session = Depends(get_db)):
    db_team = crud.get_team_by_id(db, id)
    return db_team 

@app.post("/teams/{id}/facts", response_model=schemas.Fact)
def creat_fact_for_team(id:int, fact:schemas.FactCreate, db: Session = Depends(get_db)):
    return crud.create_team_fact(db, fact, id)
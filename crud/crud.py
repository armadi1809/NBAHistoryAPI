from sqlalchemy.orm import Session 
from models import models 
from schemas import schemas
import random

def get_team(db: Session, team_id: int): 
    return db.query(models.Team).filter(models.Team.id == team_id).first()

def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()

def get_team_by_id(db: Session, id: int):
    return db.query(models.Team).filter(models.Team.id == id).first()

def get_fact_by_id(db:Session, id: int):
    return db.query(models.Fact).filter(models.Fact.id).first()

def get_random_fact(db:Session): 
    return random.choice(db.query(models.Fact).all())

def create_team(db: Session, team: schemas.Team):
    db_team = models.Team(name=team.name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team
    
# def update_team(db: Session, team: schemas.TeamUpdate):
#     db_team = db.query(models.Team).filter(models.Team.id == team.id).first()
#     db_team.historic_fact = team.historic_fact
#     db.commit()
#     db.refresh(db_team)
#     return db_team

def get_teams(db: Session, skip: int = 0, limit: int=100): 
    return db.query(models.Team).offset(skip).limit(limit).all()

def create_team_fact(db: Session, fact: schemas.FactCreate, team_id: int):
    db_fact = models.Fact(**fact.dict(), team_id=team_id)
    db.add(db_fact)
    db.commit()
    db.refresh(db_fact)
    return db_fact

def delete_fact_by_id(db:Session, id:int):
    db.query(models.Fact).filter_by(id=id).delete()
    db.commit()
    return {"Delete Operation": "Success"}
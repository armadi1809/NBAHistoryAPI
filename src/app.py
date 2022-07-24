from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models, crud, schemas
from jose import JWTError, jwt
from typing import Union
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
app = FastAPI() 

SECRET_KEY = "13fdabf0c1e2dcf5880368952cfd7dddfb36487ba8cc5a1de638b8610328c428"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
models.Base.metadata.create_all(bind=engine)

def create_access_token(expires_delta: Union[timedelta, None] = None):
    to_encode = {}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def validate_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        b = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        breakpoint()
    except JWTError: 
        raise credentials_exception
    return 1
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
def read_team(id: int, db: Session = Depends(get_db), valid_token: int = Depends(validate_token)):
    # validate_token(token)
    db_team = crud.get_team_by_id(db, id)
    return db_team 

@app.post("/teams/{id}/facts", response_model=schemas.Fact)
def creat_fact_for_team(id:int, fact:schemas.FactCreate, db: Session = Depends(get_db)):
    return crud.create_team_fact(db, fact, id)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
       expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
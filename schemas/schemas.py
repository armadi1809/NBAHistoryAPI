from pydantic import BaseModel 
from typing import List

class FactBase(BaseModel): 
    description: str = None 

class FactCreate(FactBase): 
    pass 

class Fact(FactBase): 
    id: int 
    team_id: int 
    class Config: 
        orm_mode = True

class TeamBase(BaseModel): 
    name: str 

class Team(TeamBase): 
    id: int 
    facts: List[Fact] = []
    class Config: 
        orm_mode = True 

class Token(BaseModel):
    access_token: str
    token_type: str
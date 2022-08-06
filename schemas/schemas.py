from pydantic import BaseModel 
from typing import List, Union


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    class Config:
        orm_mode = True

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


class TokenData(BaseModel):
    username: Union[str, None] = None
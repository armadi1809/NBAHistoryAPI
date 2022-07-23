from pydantic import BaseModel 

class TeamBase(BaseModel): 
    name: str 
    historic_fact: str = None 


class Team(TeamBase): 
    id: int 
    class Config: 
        orm_mode = True 

class TeamUpdate(TeamBase): 
     
    historic_fact: str
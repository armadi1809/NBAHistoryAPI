from db import Base 
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

class Team(Base): 
    __tablename__="teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True, index=True)
    historic_fact = Column(Text, nullable=False)

    
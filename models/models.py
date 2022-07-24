from db.db import Base 
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Team(Base): 
    __tablename__="teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True, index=True)
    historic_fact = Column(String, nullable=False)

    facts = relationship("Fact", back_populates="team")

class Fact(Base): 
    __tablename__="facts"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="facts")
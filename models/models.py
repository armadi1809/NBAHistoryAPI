from email.policy import default
from db.db import Base 
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Team(Base): 
    __tablename__="teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False, unique=True, index=True)
    facts = relationship("Fact", back_populates="team")

class Fact(Base): 
    __tablename__="facts"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))

    team = relationship("Team", back_populates="facts")

class User(Base):
    __tablename__="users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
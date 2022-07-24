from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#Connect to the sqlLite file located on ./sql_app.db 
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

#Creating an SQL alchemy engine to refer to it when accessing the databases later
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

#Database session 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Class to inherit from when creating the ORM classes for the databaese. 
Base = declarative_base()
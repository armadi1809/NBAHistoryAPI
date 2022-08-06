from fastapi import FastAPI
from db.db import engine 
from routers import teams, token, facts, user
from models import models

app = FastAPI()

app.include_router(teams.router)
app.include_router(token.router)
app.include_router(facts.router)
app.include_router(user.router)

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def welcomeMsg():
    return {"message": "Welcome to the NBA API: visit /docs for details about the different endpoints"}

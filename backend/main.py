from fastapi import FastAPI
from database import engine
from models import Base
from routes import users
from auth import create_access_token
from routes import auth


app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    users.router,
    prefix="/users",
    tags=["user"]
)
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)


@app.get("/health")
def health():
    return{"status":"running"}
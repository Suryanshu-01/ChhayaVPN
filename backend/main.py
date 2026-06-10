from fastapi import FastAPI
from database import engine
from models import Base
from routes import users

app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    users.router,
    prefix="/users",
    tags=["user"]
)


@app.get("/health")
def health():
    return{"status":"running"}
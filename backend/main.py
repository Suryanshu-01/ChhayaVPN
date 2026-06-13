from fastapi import FastAPI
from database import engine
from models import Base
from auth import create_access_token
from routes import auth, vpn


app=FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)


@app.get("/health")
def health():
    return{"status":"running"}

app.include_router(
    vpn.router,
    prefix="/vpn",
    tags=["VPN"]
)
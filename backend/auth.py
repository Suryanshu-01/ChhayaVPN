from dotenv import load_dotenv
from jose import JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from jose import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from database import SessionLocal
from models import Account
from sqlalchemy.orm import Session




load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth_scheme= OAuth2PasswordBearer(
    tokenUrl="auth/login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
def get_password_hash(password:str):
    return pwd_context.hash(password)

def verify_password(
        plain_password:str,
        hashed_password:str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )





def create_access_token(data: dict):
    to_encode= data.copy()
    expire = datetime.now(timezone.utc) + timedelta(hours=24)

    to_encode.update({"exp":expire})

    encoded_jwt=jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


    return encoded_jwt


def verify_access_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id= payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        return int(user_id)
    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    

def get_current_user(
        token:str=Depends(oauth_scheme),
        db:Session=Depends(get_db)
):
    user_id=verify_access_token(token)
    account=(
        db.query(Account)
        .filter(Account.id==user_id)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    return account
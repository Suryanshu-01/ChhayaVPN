from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import  Session
from database import SessionLocal
from models import Account
from schemas import AccountCreate,AccountResponse
from auth import get_password_hash,verify_password,create_access_token,get_current_user
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/signup",
    response_model=AccountResponse
)
def signup(
    account: AccountCreate,
    db: Session = Depends(get_db)
):

    existing_username = (
        db.query(Account)
        .filter(Account.username == account.username)
        .first()
    )

    if existing_username:
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        )

    existing_email = (
        db.query(Account)
        .filter(Account.email == account.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    hashed_password = get_password_hash(
        account.password
    )

    new_account = Account(
        username=account.username,
        email=account.email,
        password_hash=hashed_password
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    account=(
        db.query(Account)
        .filter(Account.email == form_data.username)
        .first()
    )

    if not account:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    if not verify_password(
        form_data.password,
        account.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    access_token=create_access_token(
        {
            "sub":str(account.id)
        }
    )
    return {
        "access_token": access_token,
        "token_type":"bearer"
    }


@router.get("/me")
def get_me(
    current_user:Account=Depends(get_current_user)
):
    return{
        "id":current_user.id,
        "username":current_user.username,
        "email":current_user.email,
        "status": current_user.status
    }
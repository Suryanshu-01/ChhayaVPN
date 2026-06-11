from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserCreate, UserResponse
from typing import List
from fastapi import HTTPException


router = APIRouter()

@router.post("/",response_model=UserResponse)
def create_user(user: UserCreate, db: Session= Depends(get_db)):
    new_user=User(
        username=user.username,
        public_key="temp_public_key",
        private_key="temp_private_key",
        ip_address="10.0.0.2"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/",response_model=List[UserResponse])
def get_users(db: Session=Depends(get_db)):
    return db.query(User).all()

@router.get("/{user_id}",response_model=UserResponse)
def get_user_by_id(user_id:int,db: Session=Depends(get_db)):
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user

@router.delete("/{user_id}")
def delete_user(user_id:int, db: Session = Depends(get_db)):
    user=db.query(User).filter(User.id== user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    db.delete(user)
    db.commit()

    return{
        "message": f"User {user.username} deleted successfully"
    }



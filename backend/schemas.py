from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username:str



class  UserResponse(BaseModel):
    id:int
    username:str
    public_key:str
    ip_address:str
    status: str
    created_at: datetime

    class Config:
        from_attributes=True




class AccountCreate(BaseModel):
    username: str
    email: str
    password: str


class AccountResponse(BaseModel):
    id: int
    username: str
    email: str
    status: str

    class Config:
        from_attributes=True


class LoginRequest(BaseModel):
    email:str
    password: str
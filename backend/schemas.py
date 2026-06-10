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
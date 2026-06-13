from pydantic import BaseModel
from datetime import datetime

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

#Future cleanup:
#Remove LoginRequest from schemas.py


class LoginRequest(BaseModel):
    email:str
    password: str

# Later we have to change it

class VPNProfileCreate(BaseModel):
    pass



class VPNProfileResponse(BaseModel):
    id: int
    owner_id: int
    public_key: str
    assigned_ip: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
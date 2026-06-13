from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime, timezone

from database import Base


class Account(Base):
    __tablename__="accounts"
    id = Column(Integer, primary_key=True, index=True)
    username= Column(String, unique= True, nullable= False)
    email= Column(String, unique= True, nullable= False)
    password_hash= Column(String, nullable=False)
    status= Column(String, default="active")

    created_at= Column(
        DateTime,
        default=lambda:datetime.now(timezone.utc)
    )




class VPNProfile(Base):
    __tablename__="vpn_profiles"
    id= Column(Integer,primary_key=True,index=True)
    owner_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    public_key=Column(String, nullable=False)
    private_key=Column(String, nullable=False)
    assigned_ip=Column(String,nullable=False)
    status = Column(
        String,
        default="active"
    )

    created_at = Column(
        DateTime,
        default=lambda:datetime.now(timezone.utc)
    )
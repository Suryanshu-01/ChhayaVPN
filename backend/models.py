from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from database import Base

class User(Base):
    __tablename__="users"

    id=Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True,nullable=False)
    public_key=Column(String,nullable=False)
    private_key=Column(String,nullable=False)
    ip_address=Column(String,nullable=False)
    status=Column(String,default="active")
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
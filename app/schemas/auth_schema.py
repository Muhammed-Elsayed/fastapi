from pydantic import BaseModel, EmailStr
from datetime import date

class AdminBase(BaseModel):
    name: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str
    join_date: date | None = None  # Add join_date with a default value of None

class AdminResponse(AdminBase):
    id: int
    join_date: date | None = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str  
    password: str

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import Session
from passlib.context import CryptContext  # encrypt library
from app.db.database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=True)
    salary = Column(Float, nullable=True)
    join_date = Column(Date, nullable=True)


class Admin(Base):
    __tablename__ = "admin"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)  # Hashed password
    join_date = Column(Date, nullable=True)

    # <Admin(id=2, username=nan)> 
    # it will return the representation of the object .
    def __str__(self):
        return f"<Admin(id={self.id}, username={self.name})>"

     # Hash password before saving
    def set_password(self, password: str):
        self.password_hash = pwd_context.hash(password)

    # Verify password
    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)



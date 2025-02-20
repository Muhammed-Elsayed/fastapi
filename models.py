from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import Session

from database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(String, nullable=True)
    salary = Column(Float, nullable=True)
    join_date = Column(Date, nullable=True)

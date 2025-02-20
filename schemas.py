from pydantic import BaseModel, EmailStr, Field
from datetime import date


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Employee's full name")
    email: EmailStr = Field(..., description="Valid email address")
    department: str | None = Field(None, max_length=50, description="Optional department name")
    salary: float | None = Field(None, ge=0, description="Salary must be non-negative")
    join_date: date | None = Field(None, description="Date of joining (optional)")

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int

    class Config:
        from_attributes = True




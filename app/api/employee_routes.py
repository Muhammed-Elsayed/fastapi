from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.crud import employee_crud as employee_crud
from app.models import models
from app.schemas import employee_schema as schemas
from app.db.database import get_db
from app.utils import get_current_user

router = APIRouter()

@router.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_admin= Depends(get_current_user) ):
    try :
        db_employee = employee_crud.create_employee(db, employee)
    except:
        raise HTTPException(status_code=404, detail="Couldn't create that user, maybe it already existed")
    return db_employee

@router.get("/employees/", response_model=list[schemas.Employee])
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_admin= Depends(get_current_user)):
    employees = employee_crud.get_employees(db, skip=skip, limit=limit)
    return employees

@router.get("/employees/{employee_id}", response_model=schemas.Employee)
def read_employee(employee_id: int, db: Session = Depends(get_db), current_admin= Depends(get_current_user)):
    db_employee = employee_crud.get_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.put("/employees/{employee_id}", response_model=schemas.Employee)
def update_employee(employee_id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db), current_admin= Depends(get_current_user)):
    db_employee = employee_crud.update_employee(db, employee_id=employee_id, employee=employee)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee

@router.delete("/employees/{employee_id}", response_model=schemas.Employee)
def delete_employee(employee_id: int, db: Session = Depends(get_db), current_admin= Depends(get_current_user)):
    db_employee = employee_crud.delete_employee(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return db_employee
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import hashlib

from database import SessionLocal, engine
import models, schemas, crud
from auth import create_token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ Root ------------------

@app.get("/")
def home():
    return {"message": "API Running Successfully"}

# ------------------ API Routes ------------------

@app.post("/register-api")
def register(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    existing = crud.get_employee_by_email(db, employee.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    return crud.create_employee(db, employee)


@app.post("/login-api")
def login(user: schemas.EmployeeLogin, db: Session = Depends(get_db)):
    db_user = crud.get_employee_by_email(db, user.email)

    if db_user and db_user.password == hashlib.sha256(user.password.encode()).hexdigest():
        token = create_token({"sub": user.email})
        return {"token": token}

    raise HTTPException(status_code=400, detail="Invalid Login")


@app.get("/employees")
def employees(db: Session = Depends(get_db)):
    return crud.get_all_employees(db)


@app.get("/employee/{id}")
def get_employee(id: int, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    return emp


@app.put("/employee/{id}")
def update_employee(id: int, employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    emp = db.query(models.Employee).filter(models.Employee.id == id).first()

    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.name = employee.name
    emp.email = employee.email
    emp.department = employee.department

    if employee.password:
        emp.password = hashlib.sha256(employee.password.encode()).hexdigest()

    db.commit()
    db.refresh(emp)

    return {"message": "Updated successfully"}


@app.delete("/employee/{id}")
def delete_employee(id: int, db: Session = Depends(get_db)):
    crud.delete_employee(db, id)
    return {"message": "Deleted successfully"}

import models
import hashlib

# ================= HASH PASSWORD =================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ================= CREATE EMPLOYEE =================
def create_employee(db, employee):
    new_emp = models.Employee(
        name=employee.name,
        email=employee.email,
        password=hash_password(employee.password),
        department=employee.department
    )

    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)

    return new_emp

# ================= LOGIN =================
def login_employee(db, email, password):
    hashed = hash_password(password)

    return db.query(models.Employee).filter(
        models.Employee.email == email,
        models.Employee.password == hashed
    ).first()

# ================= GET ALL =================
def get_all_employees(db):
    return db.query(models.Employee).all()

# ================= DELETE =================
def delete_employee(db, id):
    emp = db.query(models.Employee).filter(models.Employee.id == id).first()

    if emp:
        db.delete(emp)
        db.commit()

# ================= FIND BY EMAIL =================
def get_employee_by_email(db, email):
    return db.query(models.Employee).filter(
        models.Employee.email == email
    ).first()

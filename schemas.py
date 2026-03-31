from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    name:str
    email:str
    password:str
    department:str

class EmployeeLogin(BaseModel):
    email:str
    password:str
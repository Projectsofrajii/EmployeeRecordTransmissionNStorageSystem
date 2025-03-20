from pydantic import BaseModel, EmailStr, condecimal
from datetime import date

class EmployeeSchema(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    department: str
    designation: str
    salary: float 
    date_of_joining: date

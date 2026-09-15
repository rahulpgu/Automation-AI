import sqlite3
import sys
from pathlib import Path
import uuid
from fastapi import FastAPI, Query
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent / "enterprise-ai-assistant"
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from app.services.ai_service import AIService

app = FastAPI()
service = AIService()


class AskRequest(BaseModel):
    question: str
    session_id: str | None = None
@app.get("/")
def home():
    return {"message": "Welcome to the Employee Management API!"}

@app.get("/employees/search")
def search_employees_by_department(department: str = Query(..., description="Department to search for")):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE department = ? COLLATE NOCASE", (department,))
    rows = cursor.fetchall()
    conn.close()
    return {"department": department, "employees": rows}

@app.get("/employee")
def employee():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return {"employees": rows}
@app.get("/employee/{employee_id}")
def get_employee(employee_id: int):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=?", (employee_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"employee": row}
    else:
        return {"message": "Employee not found."}
@app.post("/employee")
def add_employee(name: str, department: str):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (name, department) VALUES (?, ?)", (name, department))
    conn.commit()
    conn.close()
    return {"message": "Employee added successfully."}
@app.get("/department")
def get_department():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT department FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return {"departments": [row[0] for row in rows]}
@app.post("/ask")
def ask(request: AskRequest):
    #session_id = request.session_id or str(uuid.uuid4)
    try:
        answer = service.ask(question=request.question,session_id=request.session_id)
        return {"answer": answer}
    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        return {"error": str(e)}



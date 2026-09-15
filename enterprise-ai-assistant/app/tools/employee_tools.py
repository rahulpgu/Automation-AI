import requests

BASE_URL = "http://127.0.0.1:8000"


def get_all_employees():
    response = requests.get(f"{BASE_URL}/employee")
    response.raise_for_status()
    return response.json()

def get_employee(employee_id):
    response = requests.get(f"{BASE_URL}/employee/{employee_id}")
    response.raise_for_status()
    return response.json()


def search_department(department: str):
    response = requests.get(
        f"{BASE_URL}/employees/search",
        params={"department": department},
    )
    response.raise_for_status()
    return response.json()


def get_departments():
    response = requests.get(f"{BASE_URL}/department")
    response.raise_for_status()
    return response.json()

def add_employee(name, department):
    response = requests.post(
        f"{BASE_URL}/employee",
        params={
            "name": name,
            "department": department
        }
    )
    response.raise_for_status()
    return response.json()

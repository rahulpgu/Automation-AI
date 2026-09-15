import requests
import json
import sqlite3
"""url = "https://jsonplaceholder.typicode.com/users/1"
response = requests.get(url)
print("Number betweek 1 and 10:")
number = int(input())
url = f"https://jsonplaceholder.typicode.com/users/{number}"
response = requests.get(url)
if response.status_code != 200:
    print("User not found.")
else:
    for resp in response.json():
        print(response.json().get('name'))
"""
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees(id INTEGER PRIMARY KEY, name TEXT, department TEXT)''')
def Add_employee(name, department):
    cursor.execute("INSERT INTO employees (name, department) VALUES (?, ?)", (name, department))
    conn.commit()
def view_employees():
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    for row in rows:
        print(row)  
def search_employee(name):
    cursor.execute("SELECT * FROM employees WHERE name=?", (name,))
    rows = cursor.fetchall()
    return rows
def exit_program():
    conn.close()
    exit()

main_menu = """
1. Add Employee
2. View Employees
3. Search Employee
4. Exit
"""
print(main_menu)
while True:
    choice = input("Enter your choice: ")
    if choice == '1':
        name = input("Enter employee name: ")
        department = input("Enter employee department: ")
        Add_employee(name, department)
        print("Employee added successfully.")
    elif choice == '2':
        view_employees()
    elif choice == '3':
        name = input("Enter employee name to search: ")
        results = search_employee(name)
        if results:
            for row in results:
                print(row)
        else:
            print("Employee not found.")
    elif choice == '4':
        exit_program()
    else:
        print("Invalid choice. Please try again.")
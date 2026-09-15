TOOL_SCHEMAS = [
    {
        "name": "get_all_employees",
        "description": "Get a list of all employees.",
        "arguments": {},
        "require_confirmation": False
    },
    {
        "name": "get_employee",
        "description": "Get an employee by their employee ID.",
        "arguments": {
            "employee_id": {
                "type": "integer",
                "description": "The employee ID."
            }
        }
    },
    {
        "name": "search_department",
        "description": "Find employees who belong to a specific department.",
        "arguments": {
            "department": {
                "type": "string",
                "description": "The department name."
            }
        }
    },
    {
        "name": "get_departments",
        "description": "Get a list of all available departments.",
        "arguments": {}
    },
    {
        "name": "add_employee",
        "description": "Add a new employee to the employee database.",
        "arguments": {
            "name": {
                "type": "string",
                "description": "The employee's name."
            },
            "department": {
                "type": "string",
                "description": "The employee's department."
            }
        },
        "require_confirmation": True
    }
]
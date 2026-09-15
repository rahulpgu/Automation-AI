from app.tools.employee_tools import (
    get_all_employees,
    get_employee,
    search_department,
    get_departments,
    add_employee
)

TOOLS = {
    "get_all_employees": {
        "function": get_all_employees,
        "require_confirmation": False,
    },
    "get_employee": {
        "function": get_employee,
        "require_confirmation": False,
    },
    "search_department": {
        "function": search_department,
        "require_confirmation": False,
    },
    "get_departments": {
        "function": get_departments,
        "require_confirmation": False,
    },
    "add_employee": {
        "function": add_employee,
        "require_confirmation": True,
    }
}

def execute_tool(tool_name, arguments,confirmed=False):
    if tool_name not in TOOLS:
        raise ValueError(f"Tool '{tool_name}' not found.")
    if require_confirmation(tool_name) and not confirmed:
        return {
            "require_confirmation": True,
            "tool": tool_name,
            "arguments": arguments
        }
    tool_function = TOOLS[tool_name]["function"]
    return tool_function(**arguments)

def require_confirmation(tool_name):
    if tool_name not in TOOLS:
        raise ValueError(f"Unknown Tool: {tool_name}")
    return TOOLS[tool_name]["require_confirmation"]
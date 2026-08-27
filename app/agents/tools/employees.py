from langchain_core.tools import tool


EMPLOYEES = [
    {
        "employee_id": "emp_001",
        "name": "John Smith",
        "role": "Cloud Consultant",
        "skills": ["AWS", "Terraform", "Kubernetes"],
        "current_project": "ACME Cloud Migration",
    },
    {
        "employee_id": "emp_002",
        "name": "John de Vries",
        "role": "Backend Engineer",
        "skills": ["Python", "FastAPI", "PostgreSQL"],
        "current_project": "Contoso API Platform",
    },
    {
        "employee_id": "emp_003",
        "name": "Alice Jansen",
        "role": "AI Engineer",
        "skills": ["Python", "RAG", "LangGraph", "Qdrant"],
        "current_project": "Globex AI Assistant",
    },
]


@tool
async def lookup_employee(name: str) -> dict:
    """
    Search the Northstar employee directory by name.

    Use this to resolve an employee's identity or retrieve basic
    directory information. Multiple employees may have the same first name.
    """

    matches = [
        employee
        for employee in EMPLOYEES
        if name.lower() in employee["name"].lower()
    ]

    if not matches:
        return {
            "status": "not_found",
            "matches": [],
        }

    if len(matches) > 1:
        return {
            "status": "ambiguous",
            "matches": matches,
        }

    return {
        "status": "found",
        "employee": matches[0],
    }


@tool
async def find_expert(skill: str) -> dict:
    """
    Find Northstar employees with expertise in a technology or skill.

    Use this when someone needs an internal expert, consultant,
    engineer, or colleague with specific technical experience.
    """

    matches = [
        employee
        for employee in EMPLOYEES
        if any(
            skill.lower() in employee_skill.lower()
            for employee_skill in employee["skills"]
        )
    ]

    return {
        "status": "found" if matches else "not_found",
        "matches": matches,
    }

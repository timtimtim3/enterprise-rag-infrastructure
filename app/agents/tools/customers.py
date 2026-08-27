from langchain_core.tools import tool


CUSTOMERS = [
    {
        "customer_id": "cus_001",
        "name": "ACME",
        "industry": "Financial Services",
    },
    {
        "customer_id": "cus_002",
        "name": "Globex",
        "industry": "Logistics",
    },
]

PROJECTS = [
    {
        "project_id": "proj_001",
        "customer_id": "cus_001",
        "name": "ACME Cloud Migration",
        "status": "active",
    },
    {
        "project_id": "proj_002",
        "customer_id": "cus_001",
        "name": "ACME Data Platform",
        "status": "completed",
    },
]


@tool
async def lookup_customer(name: str) -> dict:
    """
    Search Northstar's customer/CRM data by customer name.

    Use this when the user asks about a customer, account,
    client, or customer-specific information.
    """

    matches = [
        customer
        for customer in CUSTOMERS
        if name.lower() in customer["name"].lower()
    ]

    if not matches:
        return {"status": "not_found", "matches": []}

    if len(matches) > 1:
        return {"status": "ambiguous", "matches": matches}

    return {
        "status": "found",
        "customer": matches[0],
    }


@tool
async def get_customer_projects(customer_id: str) -> dict:
    """
    Get Northstar projects belonging to a customer.

    Requires the customer's unique customer_id. Use lookup_customer
    first when only the customer name is known.
    """

    projects = [
        project
        for project in PROJECTS
        if project["customer_id"] == customer_id
    ]

    return {
        "status": "found" if projects else "not_found",
        "projects": projects,
    }

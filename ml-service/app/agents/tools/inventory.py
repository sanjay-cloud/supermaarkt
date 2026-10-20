

check_inventory_function = {
    "type": "function",
    "name": "check_inventory",
    "description": "Check the inventory for available stock",
    "parameters": {
        "type": "object",
        "properties": {
            "id": {"type": "integer", "description": "Id of the stock item"},
        },
        "required": ["id"],
    },
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_business_info",
            "description": "Get structured business information like hours, address, phone, or pricing.",
            "parameters": {
                "type": "object",
                "properties": {
                    "field": {
                        "type": "string",
                        "enum": ["hours", "address", "phone", "pricing"],
                        "description": "The field to retrieve from business info."
                    }
                },
                "required": ["field"]
            }
        }
    }
]

def get_business_info(business_info, field):
    value = business_info.get(field, "Information not available.")
    return {"field": field, "value": value}
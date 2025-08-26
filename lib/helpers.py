import re
from tabulate import tabulate

def normalize_phone(phone: str) -> str:
    """Normalize Kenyan phone numbers to +2547XXXXXXXX format."""
    phone = phone.strip()
    if phone.startswith("07"):
        return "+254" + phone[1:]
    elif phone.startswith("+254") and len(phone) == 13:
        return phone
    else:
        raise ValueError("Invalid Kenyan phone number format")

def validate_skill(skill, skills):
    if skill not in skills:
        raise ValueError(f"Skill must be one of {skills}")
    return skill

def display_table(data, headers):
    if not data:
        print("No records found.")
        return
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

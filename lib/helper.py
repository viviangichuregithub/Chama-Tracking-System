import re
from datetime import datetime


def prompt_int(prompt: str, default=None) -> int:
    """Prompt for integer input with optional default"""
    while True:
        val = input(prompt).strip()
        if not val and default is not None:
            return default
        try:
            return int(val)
        except ValueError:
            print("❌ Please enter a valid integer.")


def prompt_float(prompt: str, default=None) -> float:
    """Prompt for float input with optional default"""
    while True:
        val = input(prompt).strip()
        if not val and default is not None:
            return default
        try:
            return float(val)
        except ValueError:
            print("❌ Please enter a valid number.")


def prompt_choice(prompt: str, choices: list, case_sensitive=False):
    """Prompt until a valid choice is given"""
    choices_display = "/".join(choices)
    while True:
        choice = input(f"{prompt} ({choices_display}): ").strip()
        if not case_sensitive:
            choice = choice.lower()
            normalized = [c.lower() for c in choices]
        else:
            normalized = choices

        if choice in normalized:
            return choices[normalized.index(choice)]
        print(f"❌ Invalid choice. Options: {choices_display}")


def normalize_phone(phone: str) -> str:
    """Convert Kenyan phone to +2547… format"""
    phone = re.sub(r"\D", "", phone)  # remove non-digits

    if phone.startswith("254"):
        phone = "+" + phone
    elif phone.startswith("07"):
        phone = "+254" + phone[1:]
    elif phone.startswith("7") and len(phone) == 9:
        phone = "+254" + phone
    elif phone.startswith("1") and len(phone) == 10:  # Safaricom, Airtel codes
        phone = "+254" + phone
    else:
        raise ValueError("Invalid Kenyan phone number format")

    if not re.match(r"^\+2547\d{8}$", phone):
        raise ValueError("Invalid Kenyan phone number format")
    return phone


def confirm_delete(name: str) -> bool:
    """Confirm delete with Y/N"""
    choice = input(f"⚠️ Are you sure you want to delete {name}? (y/n): ").strip().lower()
    return choice == "y"


def prompt_date(prompt: str, fmt="%Y-%m-%d") -> datetime:
    """Prompt user for a valid date"""
    while True:
        val = input(f"{prompt} (format {fmt}): ").strip()
        try:
            return datetime.strptime(val, fmt)
        except ValueError:
            print(f"❌ Invalid date format. Please use {fmt}.")

def print_header(title: str):
    print("\n" + "=" * 40)
    print(title)
    print("=" * 40)

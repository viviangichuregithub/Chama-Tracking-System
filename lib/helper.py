import re
from datetime import datetime


def prompt_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("❌ Please enter a valid integer.")


def prompt_choice(prompt: str, choices: list):
    """Prompt until valid choice given"""
    while True:
        choice = input(prompt).strip()
        if choice in choices:
            return choice
        print(f"❌ Invalid choice. Options: {choices}")


def normalize_phone(phone: str) -> str:
    """Convert Kenyan phone to +2547… format"""
    phone = phone.strip()
    if phone.startswith("+254"):
        return phone
    elif phone.startswith("07"):
        return "+254" + phone[1:]
    elif phone.startswith("7") and len(phone) == 9:
        return "+254" + phone
    else:
        raise ValueError("Invalid Kenyan phone number format")


def confirm_delete(name: str) -> bool:
    """Confirm delete with Y/N"""
    choice = input(f"⚠️ Are you sure you want to delete {name}? (y/n): ").lower()
    return choice == "y"

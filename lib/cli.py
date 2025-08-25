from lib.models.member import Member, MemberStatus
from lib.helper import prompt_int, prompt_choice, confirm_delete 
from lib.db.db import init_db
from tabulate import tabulate  

def main_menu():
    while True:
        print("\n=== CHAMA MAIN MENU ===")
        print("1. Members")
        print("2. Contributions")
        print("3. Loans")
        print("4. Reports")
        print("0. Exit")

        choice = prompt_choice("Select option: ", ["1", "2", "3", "4", "0"])

        if choice == "1":
            members_menu()
        elif choice == "0":
            print("👋 Goodbye!")
            break
        else:
            print("That menu is not implemented yet.")


def members_menu():
    while True:
        print("\n--- MEMBERS MENU ---")
        print("1. Create Member")
        print("2. Delete Member")
        print("3. List All Members")
        print("4. Find by ID")
        print("5. Find by Phone")
        print("6. Set Status")
        print("0. Back to Main")

        choice = prompt_choice("Choose: ", ["1", "2", "3", "4", "5", "6", "0"])

        if choice == "1":
            name = input("Enter member name: ")
            phone = input("Enter phone (07…): ")
            try:
                Member.create(name, phone)
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "2":
            member_id = prompt_int("Enter member ID to delete: ")
            member = Member.get_by_id(member_id)
            if member and confirm_delete(member.name):
                Member.delete(member_id)

        elif choice == "3":
            members = Member.get_all()
            if not members:
                print("No members found.")
            else:
                table = []
                for m in members:
                    joined = m.join_date.strftime("%Y-%m-%d %H:%M:%S") if m.join_date else "-"
                    table.append([m.id, m.name, m.phone, m.status.value, joined])
                headers = ["ID", "Name", "Phone", "Status", "Joined At"]  
                print(tabulate(table, headers=headers, tablefmt="grid"))

        elif choice == "4":
            member_id = prompt_int("Enter member ID: ")
            member = Member.get_by_id(member_id)
            if member:
                print(f"✅ Found: {member.name}, Phone: {member.phone}, Status: {member.status.value}")
            else:
                print("❌ Member not found.")

        elif choice == "5":
            phone = input("Enter phone: ")
            try:
                member = Member.find_by_phone(phone)
                if member:
                    print(f"✅ Found: {member.name}, Phone: {member.phone}, Status: {member.status.value}")
                else:
                    print("❌ No member with that phone.")
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "6":
            member_id = prompt_int("Enter member ID: ")
            member = Member.get_by_id(member_id)
            if not member:
                print("❌ Member not found.")
                continue

            print("1. ACTIVE")
            print("2. INACTIVE")
            print("3. SUSPENDED")
            status_choice = prompt_choice("Choose status: ", ["1", "2", "3"])
            status_map = {"1": MemberStatus.ACTIVE, "2": MemberStatus.INACTIVE, "3": MemberStatus.SUSPENDED}
            member.set_status(status_map[status_choice])

        elif choice == "0":
            break


if __name__ == "__main__":   
    init_db()
    main_menu()

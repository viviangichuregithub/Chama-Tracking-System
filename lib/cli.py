from lib.models.member import Member, MemberStatus
from lib.models.contribution import Contribution
from lib.models.loan import Loan, LoanStatus
from lib.models.repayment import Repayment
from lib.helper import prompt_int, prompt_choice, prompt_float, confirm_delete, print_header
from lib.db.db import init_db, SessionLocal
from tabulate import tabulate
from datetime import datetime, timedelta


# ------------------- MAIN MENU -------------------
def main_menu():
    while True:
        print_header("💰 CHAMA MAIN MENU 💸")
        print("1. Members")
        print("2. Contributions")
        print("3. Loans")
        print("4. Reports")
        print("0. Exit")

        choice = prompt_choice("Select option: ", ["1", "2", "3", "4", "0"])

        if choice == "1":
            members_menu()
        elif choice == "2":
            contributions_menu()
        elif choice == "3":
            loans_menu()
        elif choice == "4":
            reports_menu()
        elif choice == "0":
            print("👋 Thanks for Visiting My Chama! Goodbye!")
            break


# ------------------- MEMBERS MENU -------------------
def members_menu():
    while True:
        print_header("===🧑🏽‍🤝‍🧑🏾 MEMBERS MENU ===")
        print("1. Create Member")
        print("2. Delete Member")
        print("3. List All Members")
        print("4. Find by ID")
        print("5. Find by Phone")
        print("6. Set Status")
        print("0. Back to Main")

        choice = prompt_choice("Choose: ", ["1", "2", "3", "4", "5", "6", "0"])

        if choice == "1":
            name = input("Enter Member Full Name: ")
            phone = input("Enter Phone (07…): ")
            try:
                Member.create(name, phone)
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "2":
            member_id = prompt_int("Enter Member ID to delete: ")
            member = Member.get_by_id(member_id)
            if member and confirm_delete(member.name):
                Member.delete(member_id)

        elif choice == "3":
            members = Member.get_all()
            if not members:
                print("❌No Members found.")
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
            member = Member.find_by_phone(phone)
            if member:
                print(f"✅ Found: {member.name}, Phone: {member.phone}, Status: {member.status.value}")
            else:
                print("❌ No member with that phone.")

        elif choice == "6":
            member_id = prompt_int("Enter member ID: ")
            member = Member.get_by_id(member_id)
            if not member:
                print("❌ Member not found.")
                continue
            print("1. ACTIVE\n2. INACTIVE\n3. SUSPENDED")
            status_choice = prompt_choice("Choose status: ", ["1", "2", "3"])
            status_map = {"1": MemberStatus.ACTIVE, "2": MemberStatus.INACTIVE, "3": MemberStatus.SUSPENDED}
            member.set_status(status_map[status_choice])

        elif choice == "0":
            break


# ------------------- CONTRIBUTIONS MENU -------------------
def contributions_menu():
    while True:
        print_header("=== 🤑 CONTRIBUTIONS MENU ===")
        print("1. Record Contribution")
        print("2. Delete Contribution")
        print("3. List All Contributions")
        print("4. Find Contribution by ID")
        print("5. View Contribution's Member")
        print("6. Show Member Total Contributions")
        print("7. Show All Contributions for a Member")
        print("0. Back to Main")

        choice = prompt_choice("Choose: ", ["1","2","3","4","5","6","7","0"])

        if choice == "0":
            break

        elif choice == "1":
            member_id = prompt_int("Enter Member ID: ")
            amount = prompt_float("Enter Contribution amount: ")
            try:
                Contribution.create(member_id, amount)
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "2":
            contribution_id = prompt_int("Enter Contribution ID to delete: ")
            Contribution.delete(contribution_id)

        elif choice == "3":
            contributions = Contribution.get_all()
            table = []
            for c in contributions:
                date = c.date.strftime("%Y-%m-%d %H:%M:%S") if c.date else "-"
                table.append([c.id, c.member_id, c.amount, date])
            headers = ["ID", "Member ID", "Amount", "Date"]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        elif choice == "4":
            contribution_id = prompt_int("Enter Contribution ID: ")
            c = Contribution.get_by_id(contribution_id)
            if c:
                date = c.date.strftime("%Y-%m-%d %H:%M:%S") if c.date else "-"
                print(f"ID: {c.id}, Member ID: {c.member_id}, Amount: {c.amount}, Date: {date}")
            else:
                print("❌ Contribution not found.")

        elif choice == "5":
            contribution_id = prompt_int("Enter Contribution ID: ")
            c = Contribution.get_by_id(contribution_id)
            if c:
                member = Member.get_by_id(c.member_id)
                if member:
                    print(f"Contribution Member: {member.name}, Phone: {member.phone}, Status: {member.status.value}")
                else:
                    print("❌ Member not found.")

        elif choice == "6":
            member_id = prompt_int("Enter Member ID: ")
            total = Contribution.total_for_member(member_id)
            print(f"Total contributions for Member {member_id}: {total}")

        elif choice == "7":
            member_id = prompt_int("Enter Member ID: ")
            contributions = Contribution.for_member(member_id)
            if not contributions:
                print("❌ No contributions found for this member.")
            else:
                table = []
                for c in contributions:
                    date = c.date.strftime("%Y-%m-%d %H:%M:%S") if c.date else "-"
                    table.append([c.id, c.amount, date])
                headers = ["ID", "Amount", "Date"]
                print(tabulate(table, headers=headers, tablefmt="grid"))

# ------------------- LOANS MENU -------------------
def loans_menu():
    while True:
        print_header("=== 💵 LOANS MENU ===")
        print("1. Issue Loan")
        print("2. Record Loan Repayment")
        print("3. Delete Loan")
        print("4. List All Loans")
        print("5. Find Loan by ID")
        print("6. Find Loans by Status")
        print("7. View Loan's Member")
        print("0. Back to Main")

        choice = prompt_choice("Choose: ", ["1","2","3","4","5","6","7","0"])

        if choice == "0":
            break

        elif choice == "1":  # Issue Loan
            member_id = prompt_int("Enter Member ID: ")
            amount = prompt_float("Enter loan amount: ")
            print("Choose Loan Plan:")
            print("1. 1 Month (2% interest)")
            print("2. 6 Months (4% interest)")
            print("3. 12 Months (7% interest)")
            plan_choice = prompt_choice("Select plan: ", ["1","2","3"])
            plan_map = {"1": "1_month", "2": "6_months", "3": "12_months"}
            plan = plan_map[plan_choice]
            try:
                loan = Loan.issue_loan(member_id, amount, plan)
            except Exception as e:
                print(f"❌ Cannot issue loan: {e}")

        elif choice == "2":  # Record Repayment
            loan_id = prompt_int("Enter Loan ID: ")
            amount = prompt_float("Enter repayment amount: ")
            try:
                loan = Loan.get_by_id(loan_id)
                if not loan:
                    print("❌ Loan not found.")
                    continue
                loan.apply_repayment(amount)
            except Exception as e:
                print(f"❌ {e}")

        elif choice == "3":  # Delete Loan
            loan_id = prompt_int("Enter Loan ID to delete: ")
            loan = Loan.get_by_id(loan_id)
            if loan and confirm_delete(f"Loan {loan.id}"):
                session = SessionLocal()
                session.delete(session.merge(loan))
                session.commit()
                session.close()
                print(f"🚮 Loan {loan_id} deleted.")

        elif choice == "4":  # List All Loans
            loans = Loan.get_all()
            table = []
            for l in loans:
                issued = l.issued_date.strftime("%Y-%m-%d %H:%M:%S") if l.issued_date else "-"
                due = l.due_date.strftime("%Y-%m-%d %H:%M:%S") if l.due_date else "-"
                table.append([l.id, l.member_id, f"{l.amount:.2f}", f"{l.balance:.2f}", l.status.value, issued, due])
            headers = ["ID","Member ID","Amount","Balance","Status","Issued At","Due Date"]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        elif choice == "5":  # Find Loan by ID
            loan_id = prompt_int("Enter Loan ID: ")
            l = Loan.get_by_id(loan_id)
            if l:
                issued = l.issued_date.strftime("%Y-%m-%d %H:%M:%S")
                due = l.due_date.strftime("%Y-%m-%d %H:%M:%S")
                print(f"Loan {l.id}: Member {l.member_id}, Amount {l.amount:.2f}, Balance {l.balance:.2f}, "
                      f"Status {l.status.value}, Issued {issued}, Due {due}")
            else:
                print("❌ Loan not found.")

        elif choice == "6":  # Find Loans by Status
            print("1. ACTIVE\n2. PAID\n3. DEFAULTED")
            status_choice = prompt_choice("Choose status: ", ["1","2","3"])
            status_map = {"1": LoanStatus.ACTIVE, "2": LoanStatus.PAID, "3": LoanStatus.DEFAULTED}
            loans = Loan.find_by_status(status_map[status_choice])
            table = [[l.id, l.member_id, f"{l.amount:.2f}", f"{l.balance:.2f}", l.status.value] for l in loans]
            headers = ["ID","Member ID","Amount","Balance","Status"]
            print(tabulate(table, headers=headers, tablefmt="grid"))

        elif choice == "7":  # View Loan's Member
            loan_id = prompt_int("Enter Loan ID: ")
            l = Loan.get_by_id(loan_id)
            if l:
                member = Member.get_by_id(l.member_id)
                if member:
                    print(f"Loan Member: {member.name}, Phone: {member.phone}, Status: {member.status.value}")
                else:
                    print("❌ Member not found.")
            else:
                print("❌ Loan not found.")
# ------------------- REPORTS MENU -------------------
def reports_menu():
    while True:
        print_header("=== 📊 REPORTS MENU ===")
        print("1. Member Statement")
        print("2. Group Totals")
        print("3. Members in Arrears")
        print("0. Back to Main")

        choice = prompt_choice("Choose: ", ["1", "2", "3", "0"])

        if choice == "0":
            break

        elif choice == "1":  # Member Statement
            member_id = prompt_int("Enter Member ID: ")
            member = Member.get_by_id(member_id)
            if not member:
                print("❌ Member not found.")
                continue

            print(f"\nStatement for {member.name} (Phone: {member.phone}, Status: {member.status.value})")

            # Contributions
            contributions = Contribution.for_member(member_id)
            if contributions:
                table = [[c.id, f"{c.amount:.2f}", c.date.strftime("%Y-%m-%d")] for c in contributions]
                print("\nContributions:")
                print(tabulate(table, headers=["ID","Amount","Date"], tablefmt="grid"))
                total_contrib = sum(c.amount for c in contributions)
                print(f"Total Contributions: {total_contrib:.2f}")
            else:
                print("❌ No contributions found.")

            # Loans
            loans = Loan.for_member(member_id)
            if loans:
                table = [[l.id, f"{l.amount:.2f}", f"{l.balance:.2f}", l.status.value, l.due_date.strftime("%Y-%m-%d")] for l in loans]
                print("\nLoans:")
                print(tabulate(table, headers=["ID","Amount","Balance","Status","Due Date"], tablefmt="grid"))
                total_loans_member = sum(l.amount for l in loans)
                total_outstanding_member = sum(l.balance for l in loans if l.status in [LoanStatus.ACTIVE, LoanStatus.DEFAULTED])
                print(f"Total Loans: {total_loans_member:.2f}")
                print(f"Total Outstanding Balance: {total_outstanding_member:.2f}")
            else:
                print("❌ No loans found.")

        elif choice == "2":  # Group Totals
            members = Member.get_all()
            total_contributions = sum(Contribution.total_for_member(m.id) for m in members)
            total_loans = 0
            total_outstanding = 0
            for m in members:
                loans = Loan.for_member(m.id)
                total_loans += sum(l.amount for l in loans)
                total_outstanding += sum(l.balance for l in loans if l.status in [LoanStatus.ACTIVE, LoanStatus.DEFAULTED])

            print_header("--- Group Totals ---")
            print(f"Total Members: {len(members)}")
            print(f"Total Contributions: {total_contributions:.2f}")
            print(f"Total Loans Issued: {total_loans:.2f}")
            print(f"Total Outstanding Balance: {total_outstanding:.2f}")

        elif choice == "3":  # Members in Arrears
            members = Member.get_all()
            arrears_list = []
            for m in members:
                for l in Loan.for_member(m.id):
                    if l.status == LoanStatus.DEFAULTED:
                        arrears_list.append([m.id, m.name, m.phone, f"{l.balance:.2f}", l.due_date.strftime("%Y-%m-%d")])

            if arrears_list:
                print("\nMembers in Arrears:")
                print(tabulate(arrears_list, headers=["Member ID","Name","Phone","Outstanding","Due Date"], tablefmt="grid"))
            else:
                print("❌ No members in arrears.")

# ------------------- ENTRY POINT -------------------
if __name__ == "__main__":
    init_db()
    main_menu()

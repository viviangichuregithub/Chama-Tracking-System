# lib/db/seed.py
from faker import Faker
import random
from datetime import timedelta, datetime

from lib.db.db import init_db, SessionLocal
from lib.models.member import Member, MemberStatus
from lib.models.contribution import Contribution
from lib.models.loan import Loan, LoanStatus
from lib.models.repayment import Repayment
from lib.helper import normalize_phone

fake = Faker("en_US")


def seed_members(n=30):
    """Seed members into the database"""
    session = SessionLocal()
    session.query(Member).delete()
    session.commit()

    print(f"Seeding {n} members...")
    members = []

    for _ in range(n):
        name = fake.first_name() + " " + fake.last_name()
        phone = "07" + str(random.randint(10000000, 99999999))
        phone = normalize_phone(phone)
        status = random.choice(list(MemberStatus))

        member = Member(name=name, phone=phone, status=status)
        session.add(member)
        session.flush()  # ensure member.id is generated
        members.append(member)

    session.commit()
    print("✅ Members seeded!")
    return members


def seed_contributions(members, n=50):
    """Seed contributions for random members"""
    session = SessionLocal()
    session.query(Contribution).delete()
    session.commit()

    print(f"Seeding {n} contributions...")
    for _ in range(n):
        member = random.choice(members)
        amount = round(random.uniform(100, 5000), 2)
        date = fake.date_time_this_year()

        contribution = Contribution(member_id=member.id, amount=amount, date=date)
        session.add(contribution)

    session.commit()
    print("✅ Contributions seeded!")


def seed_loans(members, n=15):
    """Seed loans respecting one-loan-per-member and contribution limits"""
    session = SessionLocal()
    session.query(Loan).delete()
    session.commit()

    print(f"Seeding up to {n} loans...")
    loans = []

    total_chama_contributions = sum(Contribution.total_for_member(m.id) for m in members)

    attempts = 0
    while len(loans) < n and attempts < n*5:
        attempts += 1
        member = random.choice(members)
        member_contrib = Contribution.total_for_member(member.id)

        if member_contrib <= 0:
            continue  # skip members without contributions

        # Skip members who already have an active/defaulted loan
        existing_loans = [l for l in Loan.for_member(member.id) if l.status in [LoanStatus.ACTIVE, LoanStatus.DEFAULTED]]
        if existing_loans:
            continue

        # Max loan amount
        max_member_loan = 3 * member_contrib
        current_total_loans = sum(
            l.balance for m2 in members for l in Loan.for_member(m2.id)
            if l.status in [LoanStatus.ACTIVE, LoanStatus.DEFAULTED]
        )
        max_allowed = min(max_member_loan, 0.5 * total_chama_contributions - current_total_loans)
        if max_allowed <= 0:
            continue

        amount = round(random.uniform(100, max_allowed), 2)
        issued_date = fake.date_time_this_year()
        plan_choice = random.choice([30, 180, 365])
        due_date = issued_date + timedelta(days=plan_choice)
        interest_rate = {30: 2.0, 180: 4.0, 365: 7.0}[plan_choice]
        term_years = (due_date - issued_date).days / 365
        total_balance = round(amount + (amount * interest_rate * term_years / 100), 2)

        loan = Loan(
            member_id=member.id,
            amount=amount,
            issued_date=issued_date,
            due_date=due_date,
            interest_rate=interest_rate,
            balance=total_balance,
            status=LoanStatus.ACTIVE
        )
        session.add(loan)
        session.flush()
        loans.append(loan)

    session.commit()
    print(f"✅ Loans seeded! Total loans created: {len(loans)}")
    return loans


def seed_repayments(loans, n=15):
    """Seed repayments against existing loans using apply_repayment"""
    session = SessionLocal()
    session.query(Repayment).delete()
    session.commit()

    print(f"Seeding {n} repayments...")
    for _ in range(n):
        loan = random.choice(loans)
        if loan.balance <= 0:
            continue  # skip fully repaid loans

        amount = round(random.uniform(100, float(loan.balance)), 2)
        date = fake.date_time_between(start_date=loan.issued_date, end_date=datetime.now())

        repayment = Repayment(loan_id=loan.id, amount=amount, date=date)
        session.add(repayment)

        # Apply repayment via the method
        loan.apply_repayment(amount)
        session.add(loan)

    session.commit()
    print("✅ Repayments seeded!")


if __name__ == "__main__":
    init_db()
    members = seed_members(30)
    seed_contributions(members, 50)
    loans = seed_loans(members, 15)
    seed_repayments(loans, 15)
    print("🎉 Database seeding complete!")

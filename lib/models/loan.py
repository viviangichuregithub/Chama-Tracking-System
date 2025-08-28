# lib/models/loan.py
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, Enum
from datetime import datetime, timedelta
import enum
from lib.db.db import Base, SessionLocal
from lib.models.member import Member
from lib.models.contribution import Contribution

def now():
    """Return current datetime without microseconds."""
    return datetime.now().replace(microsecond=0)

class LoanStatus(enum.Enum):
    ACTIVE = "ACTIVE"       # Currently paying
    PAID = "PAID"           # Fully repaid
    DEFAULTED = "DEFAULTED" # Missed deadline with remaining balance

class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Float, nullable=False)
    issued_date = Column(DateTime, default=now)
    due_date = Column(DateTime, nullable=False)
    interest_rate = Column(Float, nullable=False)  # Stored as percentage
    status = Column(Enum(LoanStatus), default=LoanStatus.ACTIVE)
    balance = Column(Float, nullable=False)

    # ---------------- Methods ----------------
    @classmethod
    def issue_loan(cls, member_id: int, amount: float, plan: str):
        """
        Issue a loan with automatic due date and interest rate based on plan.
        Plans:
        - '1_month': 1 month, 2% interest
        - '6_months': 6 months, 4% interest
        - '12_months': 1 year, 7% interest
        """
        plan_options = {
            "1_month": {"days": 30, "rate": 0.02},
            "6_months": {"days": 180, "rate": 0.04},
            "12_months": {"days": 365, "rate": 0.07}
        }

        if plan not in plan_options:
            raise ValueError("❌ Invalid plan. Choose '1_month', '6_months', or '12_months'.")

        session = SessionLocal()
        try:
            member = session.get(Member, member_id)
            if not member:
                raise ValueError("❌ Member not found.")

            # Rule 1: Minimum 2 months membership
            if member.join_date > datetime.now() - timedelta(days=60):
                raise ValueError(
                    f"❌ Cannot lend loan. Member must be at least 2 months in the chama "
                    f"(Joined {member.join_date.date()})."
                )

            # Rule 2: Only one active loan at a time
            active_loans = session.query(cls).filter_by(member_id=member_id, status=LoanStatus.ACTIVE).all()
            if active_loans:
                raise ValueError(
                    f"❌ Cannot lend loan. Member has an active loan (ID {active_loans[0].id}). Finish repayment first."
                )

            # Rule 3: Loan amount <= 3 * total contributions for this member
            total_contrib_member = Contribution.total_for_member(member_id)
            if amount > 3 * total_contrib_member:
                raise ValueError(
                    f"❌ Cannot lend loan. Requested amount {amount:.2f} exceeds 3× member contributions ({3*total_contrib_member:.2f})."
                )

            if amount <= 0:
                raise ValueError("❌ Loan must be greater than 0.")

            # Rule 4: Total loans for all members <= total chama contributions
            all_members = session.query(Member).all()
            total_chama_contrib = sum(Contribution.total_for_member(m.id) for m in all_members)
            total_outstanding_loans = sum(
                sum(l.balance for l in session.query(cls).filter(cls.member_id==m.id,
                                                                 cls.status.in_([LoanStatus.ACTIVE, LoanStatus.DEFAULTED])).all())
                for m in all_members
            )

            if total_outstanding_loans + amount > total_chama_contrib:
                raise ValueError(
                    f"❌ Cannot lend loan. Total loans ({total_outstanding_loans + amount:.2f}) "
                    f"❌ Not possible as it would surpass the total chama contributions ({total_chama_contrib:.2f})."
                )

            # Determine due date and interest
            plan_data = plan_options[plan]
            due_date = now() + timedelta(days=plan_data["days"])
            interest_rate = plan_data["rate"]

            # Calculate total balance
            total_balance = round(amount + (amount * interest_rate), 2)
            amount = round(amount, 2)

            loan = cls(
                member_id=member_id,
                amount=amount,
                due_date=due_date,
                balance=total_balance,
                interest_rate=round(interest_rate * 100, 2),  # store as percentage
                status=LoanStatus.ACTIVE
            )
            session.add(loan)
            session.commit()
            print(f"Loan of {amount:.2f} issued to Member {member_id} with plan '{plan}', "
                  f"interest {interest_rate*100:.2f}%, balance {loan.balance:.2f}, due {due_date.date()}")
            return loan
        finally:
            session.close()

    def apply_repayment(self, amount: float):
        """Apply repayment and automatically set status."""
        if amount <= 0:
            raise ValueError("❌ Repayment must be greater than 0.")

        session = SessionLocal()
        try:
            loan = session.merge(self)
            if amount > loan.balance:
                raise ValueError("❌ Repayment cannot exceed remaining balance.")
            loan.balance -= amount

            loan.balance = round(loan.balance, 2)

            if loan.balance <= 0:
                loan.balance = 0
                loan.status = LoanStatus.PAID
            elif loan.due_date < now() and loan.balance > 0:
                loan.status = LoanStatus.DEFAULTED
            else:
                loan.status = LoanStatus.ACTIVE

            session.commit()
            print(f"Repayment of {amount:.2f} applied. New balance: {loan.balance:.2f}, Status: {loan.status.value}")
        finally:
            session.close()

    # ---------------- Class Methods ----------------
    @classmethod
    def get_all(cls):
        session = SessionLocal()
        try:
            return session.query(cls).all()
        finally:
            session.close()

    @classmethod
    def get_by_id(cls, loan_id: int):
        session = SessionLocal()
        try:
            return session.get(cls, loan_id)
        finally:
            session.close()

    @classmethod
    def for_member(cls, member_id: int):
        session = SessionLocal()
        try:
            return session.query(cls).filter_by(member_id=member_id).all()
        finally:
            session.close()

    @classmethod
    def find_by_status(cls, status: LoanStatus):
        session = SessionLocal()
        try:
            return session.query(cls).filter_by(status=status).all()
        finally:
            session.close()

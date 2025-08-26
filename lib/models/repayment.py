# lib/models/repayment.py
from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from datetime import datetime
from lib.db.db import Base, SessionLocal
from lib.models.loan import Loan

# Function to get current datetime without microseconds
def now():
    return datetime.now().replace(microsecond=0)

class Repayment(Base):
    __tablename__ = "repayments"

    id = Column(Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey("loans.id"), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, default=now)

    # --- Methods ---
    @classmethod
    def apply_repayment(cls, loan_id: int, amount: float):
        """Apply repayment to a loan safely"""
        if amount <= 0:
            raise ValueError("Repayment must be greater than 0.")

        session = SessionLocal()
        loan = session.get(Loan, loan_id)
        if not loan:
            raise ValueError("Loan not found.")
        if amount > loan.balance:
            raise ValueError("Repayment cannot exceed loan balance.")

        # Create repayment record and apply to loan
        repayment = cls(loan_id=loan_id, amount=amount, date=now())
        loan.apply_repayment(amount)  # Updates balance and status

        session.add(repayment)
        session.commit()
        print(f"Repayment of {amount} applied to Loan {loan_id}, new balance {loan.balance}")
        return repayment

    @classmethod
    def get_all(cls):
        session = SessionLocal()
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, repayment_id: int):
        session = SessionLocal()
        return session.get(cls, repayment_id)

    @classmethod
    def for_loan(cls, loan_id: int):
        session = SessionLocal()
        return session.query(cls).filter_by(loan_id=loan_id).all()

    # --- Debug helper ---
    def __repr__(self):
        return f"<Repayment id={self.id}, loan_id={self.loan_id}, amount={self.amount}, date={self.date}>"

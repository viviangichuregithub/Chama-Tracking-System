from sqlalchemy import Column, Integer, ForeignKey, Numeric, DateTime
from datetime import datetime
from lib.db.db import Base, SessionLocal

# Function to get current datetime without microseconds
def now():
    return datetime.now().replace(microsecond=0)

class Contribution(Base):
    __tablename__ = "contributions"

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    date = Column(DateTime, default=now)  # clean timestamp

    # --- Methods ---
    @classmethod
    def create(cls, member_id: int, amount: float):
        """Add to existing contribution today or create new record"""
        if amount <= 0:
            raise ValueError("Contribution must be greater than 0.")

        session = SessionLocal()
        today = now().date()

        # Check if member already has contribution today
        existing = session.query(cls).filter(
            cls.member_id == member_id,
            cls.date.cast(DateTime).between(datetime.combine(today, datetime.min.time()),
                                            datetime.combine(today, datetime.max.time()))
        ).first()

        if existing:
            existing.amount += amount
            session.commit()
            print(f"Added {amount} to existing contribution (ID {existing.id}) for Member ID {member_id}. New total: {existing.amount}")
            return existing
        else:
            contribution = cls(member_id=member_id, amount=amount, date=now())
            session.add(contribution)
            session.commit()
            print(f"Contribution of {amount} recorded for Member ID {member_id} (ID {contribution.id})")
            return contribution

    @classmethod
    def delete(cls, contribution_id: int):
        session = SessionLocal()
        c = session.get(cls, contribution_id)
        if not c:
            print("❌ Contribution not found.")
            return False
        session.delete(c)
        session.commit()
        print(f"🗑 Contribution {contribution_id} deleted.")
        return True

    @classmethod
    def get_all(cls):
        session = SessionLocal()
        return session.query(cls).all()

    @classmethod
    def get_by_id(cls, contribution_id: int):
        session = SessionLocal()
        return session.get(cls, contribution_id)

    @classmethod
    def for_member(cls, member_id: int):
        session = SessionLocal()
        return session.query(cls).filter_by(member_id=member_id).all()

    @classmethod
    def total_for_member(cls, member_id: int):
        session = SessionLocal()
        total = session.query(cls).filter_by(member_id=member_id).with_entities(cls.amount).all()
        return sum([float(a[0]) for a in total]) if total else 0.0

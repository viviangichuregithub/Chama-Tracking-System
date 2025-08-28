# lib/models/member.py
from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
import enum

from lib.db.db import Base, SessionLocal
from lib.helper import normalize_phone

def now():
    return datetime.now().replace(microsecond=0)

class MemberStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"

class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    join_date = Column(DateTime, default=now)  
    status = Column(Enum(MemberStatus), default=MemberStatus.ACTIVE)

    # Methods
    @classmethod
    def create(cls, name: str, phone: str, status=MemberStatus.ACTIVE):
        if len(name.strip()) < 2:
            raise ValueError("❌ Name must be at least 2 characters long.")
        phone = normalize_phone(phone)

        with SessionLocal() as session:
            member = cls(name=name.strip(), phone=phone, status=status, join_date=now())
            session.add(member)
            session.commit()
            session.refresh(member)  # ensures ID is populated
            print(
                f"✅ Member '{name}' created with ID {member.id} | Join Date: {member.join_date}"
            )
            return member

    @classmethod
    def delete(cls, member_id: int):
        with SessionLocal() as session:
            member = session.get(cls, member_id)
            if not member:
                print("❌ Member not found.")
                return False
            session.delete(member)
            session.commit()
            print(f"🚮 Member {member.name} deleted.")
            return True

    @classmethod
    def get_all(cls):
        with SessionLocal() as session:
            return session.query(cls).all()

    @classmethod
    def get_by_id(cls, member_id: int):
        with SessionLocal() as session:
            return session.get(cls, member_id)

    @classmethod
    def find_by_phone(cls, phone: str):
        phone = normalize_phone(phone)
        with SessionLocal() as session:
            return session.query(cls).filter_by(phone=phone).first()

    def set_status(self, status: MemberStatus):
        """Update member status safely."""
        with SessionLocal() as session:
            managed_member = session.merge(self)
            managed_member.status = status
            session.commit()
            print(f"✅ Status for {managed_member.name} set to {status.value}")

    @classmethod
    def active(cls):
        with SessionLocal() as session:
            return session.query(cls).filter_by(status=MemberStatus.ACTIVE).all()

    # Debug helper
    def __repr__(self):
        return f"<Member id={self.id}, name='{self.name}', phone='{self.phone}', status={self.status.value}, join_date={self.join_date}>"

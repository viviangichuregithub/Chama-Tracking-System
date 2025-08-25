from faker import Faker
import random

from lib.db.db import init_db, SessionLocal
from lib.models.member import Member, MemberStatus
from lib.helper import normalize_phone

fake = Faker("en_US") 


def seed_members(n=10):
    session = SessionLocal()

    # Clean existing
    session.query(Member).delete()
    session.commit()

    print(f"Seeding {n} members...")

    for _ in range(n):
        # Fake Kenyan-style name
        name = fake.first_name() + " " + fake.last_name()

        # Fake phone (Kenyan format 07…)
        phone = "07" + str(random.randint(10000000, 99999999))
        phone = normalize_phone(phone)

        status = random.choice(list(MemberStatus))
        member = Member(name=name, phone=phone, status=status)

        session.add(member)

    session.commit()
    print("Members seeded!")


if __name__ == "__main__":
    init_db()
    seed_members(15)  # generate 15 members

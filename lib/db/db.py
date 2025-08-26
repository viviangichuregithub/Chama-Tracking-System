from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database
engine = create_engine("sqlite:///chama.db", echo=False)

# Base for all models
Base = declarative_base()

# Session factory with expire_on_commit=False to prevent detached objects
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)


def init_db():
    """Create all tables"""
    # Import all models here to ensure they are registered with Base
    from lib.models.member import Member
    from lib.models.contribution import Contribution
    from lib.models.loan import Loan
    from lib.models.repayment import Repayment

    Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database
engine = create_engine("sqlite:///chama.db", echo=False)

# Base for all models
Base = declarative_base()

# Session factory
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Create all tables"""
    from lib.models.member import Member  # import here to avoid circular imports
    Base.metadata.create_all(engine)

from config import DATABASE_URL
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
try:
    engine = create_engine(
        DATABASE_URL
    )

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    import traceback

    traceback.print_exc()
    print(e)
    print("DB connection failed")


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
        db.commit()
    except Exception:
        if db:
            db.rollback()
    finally:
        if db:
            db.close()

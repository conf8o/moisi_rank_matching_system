from config import DATABASE_URL
from typing import Generator, Callable
from sqlalchemy import create_engine, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ID = String

Base = declarative_base()
try:
    engine = create_engine(
        DATABASE_URL,
        echo=True
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

def repository(Repository) -> Callable:


    return get_db

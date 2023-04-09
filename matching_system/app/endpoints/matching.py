from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


@router.post("/entries")
def create_entry(db: Session = Depends(get_db)):
    return ""

@router.get("/entries")
def query_entry(db: Session = Depends(get_db)):
    return ""


@router.get("/matching")
def query_matching(db: Session = Depends(get_db)):
    return ""

@router.post("/match_making")
def read_root(db: Session = Depends(get_db)):

    return str(db)

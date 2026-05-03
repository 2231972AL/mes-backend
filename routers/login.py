from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import login_pin
from database import get_db

router = APIRouter(
    prefix="/login",
    tags=["Login"]
)

@router.post("/")
def login(pin: str, db: Session = Depends(get_db)):
    return login_pin(pin, db)

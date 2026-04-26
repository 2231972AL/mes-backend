from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Utente

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    # Controllo username duplicato
    existing = db.query(Utente).filter(Utente.username == username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username già esistente")

    user = Utente(
        username=username,
        password=password,
        attivo=1
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/")
def list_users(db: Session = Depends(get_db)):
    return db.query(Utente).all()

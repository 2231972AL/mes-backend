from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Utente
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ---------------------------------------------------------
# LISTA UTENTI
# ---------------------------------------------------------
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    utenti = db.query(Utente).all()
    return utenti


# ---------------------------------------------------------
# OTTIENI UTENTE PER ID
# ---------------------------------------------------------
@router.get("/{utente_id}")
def get_user(utente_id: int, db: Session = Depends(get_db)):
    utente = db.query(Utente).filter(Utente.id == utente_id).first()

    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    return utente


# ---------------------------------------------------------
# CREA NUOVO UTENTE
# ---------------------------------------------------------
@router.post("/")
def create_user(nome: str, ruolo: str, pin: str, db: Session = Depends(get_db)):
    nuovo = Utente(nome=nome, ruolo=ruolo, pin=pin)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


# ---------------------------------------------------------
# ELIMINA UTENTE
# ---------------------------------------------------------
@router.delete("/{utente_id}")
def delete_user(utente_id: int, db: Session = Depends(get_db)):
    utente = db.query(Utente).filter(Utente.id == utente_id).first()

    if not utente:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    db.delete(utente)
    db.commit()
    return {"detail": "Utente eliminato"}

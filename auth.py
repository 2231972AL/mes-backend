from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models import Utente, Sessione
from utils.security import create_token
from database import get_db

def login(username: str, password: str, db: Session = Depends(get_db)):
    # Cerca l'utente corretto
    user = db.query(Utente).filter(
        Utente.username == username,
        Utente.password == password,
        Utente.attivo == 1
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Credenziali errate")

    # Crea token
    token = create_token()

    sessione = Sessione(
        user_id=user.id,
        token=token
    )

    db.add(sessione)
    db.commit()
    db.refresh(sessione)

    return {
        "access_token": token,
        "user_id": user.id
    }


def get_user_from_token_db(token: str, db: Session = Depends(get_db)):
    sessione = db.query(Sessione).filter(Sessione.token == token).first()
    if not sessione:
        raise HTTPException(status_code=401, detail="Token non valido")

    user = db.query(Utente).filter(Utente.id == sessione.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Utente non trovato")

    return user

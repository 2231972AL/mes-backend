import hashlib
import uuid
from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Utente, Sessione
from datetime import datetime

def hash_pin(pin: str) -> str:
    return hashlib.sha256(pin.encode()).hexdigest()

def verify_pin(pin: str, hashed_pin: str) -> bool:
    return hash_pin(pin) == hashed_pin

def create_token() -> str:
    return str(uuid.uuid4())

def get_Utente_from_token(
    token: str = Header(None),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Token mancante")

    sessione = (
        db.query(Sessione)
        .filter(Sessione.token == token, Sessione.attiva == True)
        .first()
    )
    if not sessione:
        raise HTTPException(status_code=401, detail="Sessione non valida")

    sessione.last_activity = datetime.utcnow()
    db.commit()
    return sessione.Utente


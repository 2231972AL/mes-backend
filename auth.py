import uuid
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models import Utente
from database import get_db

# ---------------------------------------------------------
# LOGIN CON PIN
# ---------------------------------------------------------
def login_pin(pin: str, db: Session):
    user = db.query(Utente).filter(Utente.pin == pin).first()

    if not user:
        raise HTTPException(status_code=401, detail="PIN non valido")

    # Genera token
    token = str(uuid.uuid4())

    # Salva il token nel DB
    user.token = token
    db.commit()

    return {
        "token": token,
        "nome": user.nome,
        "ruolo": user.ruolo
    }


# ---------------------------------------------------------
# VALIDAZIONE TOKEN PER ENDPOINT PROTETTI
# ---------------------------------------------------------
def get_user_from_token_db(token: str, db: Session = Depends(get_db)):
    user = db.query(Utente).filter(Utente.token == token).first()

    if not user:
        raise HTTPException(status_code=401, detail="Token non valido")

    return user

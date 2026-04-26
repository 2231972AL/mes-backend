import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User

def login_pin(pin: str, db: Session):
    user = db.query(User).filter(User.pin == pin).first()

    if not user:
        raise HTTPException(status_code=401, detail="PIN non valido")

    token = str(uuid.uuid4())

    return {
        "token": token,
        "nome": user.nome,
        "ruolo": user.ruolo
    }

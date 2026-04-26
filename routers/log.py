from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import LogLavorazione
from auth import get_user_from_token_db

router = APIRouter(prefix="/log", tags=["Log"])


# ---------------------------------------------------------
# REGISTRA MINUTI LAVORATI
# ---------------------------------------------------------
@router.post("/")
def registra_minuti(payload: dict, db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    log = LogLavorazione(
        commessa_id=payload["commessa_id"],
        fase_id=payload.get("fase_id"),
        operatore_id=payload.get("operatore_id"),
        minuti=payload["minuti"],
        azione="minuti_lavorati"
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"successo": True, "id": log.id}

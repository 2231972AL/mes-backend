from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Fase, LogLavorazione
from datetime import datetime

router = APIRouter(prefix="/timer", tags=["Timer"])

@router.post("/start/{fase_id}")
def start_timer(fase_id: int, db: Session = Depends(get_db)):
    fase = db.query(Fase).filter(Fase.id == fase_id).first()
    if not fase:
        return {"errore": "Fase non trovata"}

    log = LogLavorazione(
        commessa_id=fase.commessa_id,
        fase_id=fase.id,
        operatore_id=None,
        azione="start",
        timestamp=datetime.utcnow()
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return {"successo": True, "log_id": log.id}


@router.post("/stop/{fase_id}")
def stop_timer(fase_id: int, db: Session = Depends(get_db)):
    fase = db.query(Fase).filter(Fase.id == fase_id).first()
    if not fase:
        return {"errore": "Fase non trovata"}

    start_log = (
        db.query(LogLavorazione)
        .filter(LogLavorazione.fase_id == fase_id, LogLavorazione.azione == "start")
        .order_by(LogLavorazione.timestamp.desc())
        .first()
    )

    if not start_log:
        return {"errore": "Nessun timer avviato"}

    stop_time = datetime.utcnow()
    minuti = int((stop_time - start_log.timestamp).total_seconds() / 60)

    stop_log = LogLavorazione(
        commessa_id=fase.commessa_id,
        fase_id=fase.id,
        operatore_id=None,
        azione="stop",
        minuti=minuti,
        timestamp=stop_time
    )

    db.add(stop_log)
    db.commit()

    return {"successo": True, "minuti_registrati": minuti}
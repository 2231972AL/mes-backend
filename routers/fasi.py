from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Fase, LogLavorazione
from auth import get_user_from_token_db

router = APIRouter(prefix="/fasi", tags=["Fasi"])


# ---------------------------------------------------------
# CREA FASE
# ---------------------------------------------------------
@router.post("/")
def crea_fase(payload: dict, db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    fase = Fase(
        commessa_id=payload["commessa_id"],
        nome=payload["nome"],
        tempo_previsto=payload.get("tempo_previsto"),
        stato="da_fare"
    )
    db.add(fase)
    db.commit()
    db.refresh(fase)
    return {"successo": True, "id": fase.id}


# ---------------------------------------------------------
# MODIFICA FASE
# ---------------------------------------------------------
@router.put("/{id}")
def modifica_fase(id: int, payload: dict, db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    fase = db.query(Fase).filter(Fase.id == id).first()
    if not fase:
        return {"errore": "Fase non trovata"}

    fase.nome = payload.get("nome", fase.nome)
    fase.tempo_previsto = payload.get("tempo_previsto", fase.tempo_previsto)

    db.commit()
    return {"successo": True}


# ---------------------------------------------------------
# CAMBIO STATO FASE + LOG AUTOMATICO
# ---------------------------------------------------------
@router.put("/{id}/stato")
def cambia_stato_fase(id: int, payload: dict, db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    fase = db.query(Fase).filter(Fase.id == id).first()
    if not fase:
        return {"errore": "Fase non trovata"}

    nuovo_stato = payload.get("stato")
    operatore_id = payload.get("operatore_id")

    fase.stato = nuovo_stato

    # LOG AUTOMATICO
    log = LogLavorazione(
        commessa_id=fase.commessa_id,
        fase_id=fase.id,
        operatore_id=operatore_id,
        azione=f"fase_{nuovo_stato}",
        minuti=None
    )
    db.add(log)

    db.commit()
    return {"successo": True}

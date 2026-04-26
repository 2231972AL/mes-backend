from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Commessa, Fase, LogLavorazione, Utente
from auth import get_user_from_token_db

router = APIRouter(prefix="/commesse", tags=["Commesse"])


# ---------------------------------------------------------
# LISTA COMMESSE
# ---------------------------------------------------------
@router.get("/")
def lista_commesse(db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    commesse = db.query(Commessa).all()
    return [
        {
            "id": c.id,
            "codice": c.codice,
            "descrizione": c.descrizione,
            "stato": c.stato,
            "operatore_id": c.operatore_id
        }
        for c in commesse
    ]


# ---------------------------------------------------------
# DETTAGLIO COMMESSA (fasi + log)
# ---------------------------------------------------------
@router.get("/{id}")
def dettaglio_commessa(id: int, db: Session = Depends(get_db), user=Depends(get_user_from_token_db)):
    commessa = db.query(Commessa).filter(Commessa.id == id).first()
    if not commessa:
        return {"errore": "Commessa non trovata"}

    # Fasi
    fasi = [
        {
            "id": f.id,
            "nome": f.nome,
            "tempo_previsto": f.tempo_previsto,
            "stato": f.stato
        }
        for f in commessa.fasi
    ]

    # Log
    logs = [
        {
            "id": l.id,
            "fase_id": l.fase_id,
            "operatore_id": l.operatore_id,
            "azione": l.azione,
            "minuti": l.minuti,
            "timestamp": l.timestamp
        }
        for l in commessa.log
    ]

    return {
        "id": commessa.id,
        "codice": commessa.codice,
        "descrizione": commessa.descrizione,
        "stato": commessa.stato,
        "operatore_id": commessa.operatore_id,
        "ora_inizio": commessa.ora_inizio,
        "ora_fine": commessa.ora_fine,
        "note": commessa.note,
        "fasi": fasi,
        "logs": logs
    }


# ---------------------------------------------------------
# CAMBIO STATO COMMESSA + LOG AUTOMATICO
# ---------------------------------------------------------
@router.put("/{id}/stato")
def aggiorna_stato_commessa(
    id: int,
    payload: dict,
    db: Session = Depends(get_db),
    user=Depends(get_user_from_token_db)
):
    commessa = db.query(Commessa).filter(Commessa.id == id).first()
    if not commessa:
        return {"errore": "Commessa non trovata"}

    nuovo_stato = payload.get("stato")
    operatore_id = payload.get("operatore_id")

    commessa.stato = nuovo_stato

    if nuovo_stato == "in_lavorazione":
        commessa.operatore_id = operatore_id
        if commessa.ora_inizio is None:
            commessa.ora_inizio = datetime.utcnow()

    if nuovo_stato == "completata":
        commessa.ora_fine = datetime.utcnow()

    # LOG AUTOMATICO
    log = LogLavorazione(
        commessa_id=id,
        fase_id=None,
        operatore_id=operatore_id,
        azione=f"commessa_{nuovo_stato}",
        minuti=None
    )
    db.add(log)

    db.commit()
    return {"successo": True}

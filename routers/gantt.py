from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Commessa, Fase

router = APIRouter(prefix="/gantt", tags=["Gantt"])

@router.get("/{commessa_id}")
def gantt_commessa(commessa_id: int, db: Session = Depends(get_db), user=Depends()):
    commessa = db.query(Commessa).filter(Commessa.id == commessa_id).first()
    if not commessa:
        return {"errore": "Commessa non trovata"}

    fasi = db.query(Fase).filter(Fase.commessa_id == commessa_id).all()

    gantt_data = []
    for f in fasi:
        gantt_data.append({
            "fase": f.nome,
            "stato": f.stato,
            "start_previsto": f.start_previsto,
            "end_previsto": f.end_previsto,
            "tempo_previsto": f.tempo_previsto,
            "tempo_reale": f.tempo_reale
        })

    return {
        "commessa": commessa.codice,
        "stato": commessa.stato,
        "fasi": gantt_data
    }

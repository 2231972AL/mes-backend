from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from database import get_db

router = APIRouter(prefix="/lotti", tags=["Lotti"])

@router.get("/")
def lista_lotti(db: Session = Depends(get_db), user=Depends()):
    return db.query(Lotto).all()

@router.get("/materiale/{materiale_id}")
def lotti_per_materiale(materiale_id: int, db: Session = Depends(get_db), user=Depends()):
    return db.query(Lotto).filter(Lotto.materiale_id == materiale_id).all()

@router.get("/{lotto_id}/certificato")
def scarica_certificato(lotto_id: int, db: Session = Depends(get_db), user=Depends()):
    lotto = db.query(Lotto).filter(Lotto.id == lotto_id).first()
    if not lotto or not lotto.certificato_path:
        return {"errore": "Certificato non disponibile"}

    return FileResponse(lotto.certificato_path, media_type="application/pdf")

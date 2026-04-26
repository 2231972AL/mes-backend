from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from datetime import datetime
import shutil
import os

router = APIRouter(prefix="/materiali", tags=["Materiali"])

@router.get("/")
def lista_materiali(db: Session = Depends(get_db)):
    return db.query(Materiale).all()

@router.post("/")
def crea_materiale(nome: str, spessore: float, giacenza: int, db: Session = Depends(get_db), user=Depends()):
    nuovo = Materiale(nome=nome, spessore=spessore, giacenza=giacenza)
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo

@router.post("/{materiale_id}/lotti")
def crea_lotto(materiale_id: int, quantita: int, certificato: UploadFile = File(None), db: Session = Depends(get_db), user=Depends()):
    certificato_path = None

    if certificato:
        folder = "static/certificati"
        os.makedirs(folder, exist_ok=True)
        certificato_path = f"{folder}/{datetime.utcnow().timestamp()}_{certificato.filename}"

        with open(certificato_path, "wb") as buffer:
            shutil.copyfileobj(certificato.file, buffer)

    lotto = Lotto(
        materiale_id=materiale_id,
        quantita=quantita,
        certificato_path=certificato_path
    )

    db.add(lotto)
    db.commit()
    db.refresh(lotto)
    return lotto

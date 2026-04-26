from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/kpi", tags=["KPI"])


@router.get("/operatori")
def kpi_operatori(db: Session = Depends(get_db)):
    # Endpoint placeholder: qui in futuro potrai calcolare i KPI reali
    return {
        "messaggio": "KPI operatori non ancora implementati",
        "dettaglio": []
    }


@router.get("/produzione")
def kpi_produzione(db: Session = Depends(get_db)):
    # Altro placeholder per KPI di produzione
    return {
        "messaggio": "KPI produzione non ancora implementati",
        "dettaglio": []
    }

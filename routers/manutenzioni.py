from fastapi import APIRouter

router = APIRouter(prefix="/manutenzioni", tags=["Manutenzioni"])

@router.get("/")
def manutenzioni_placeholder():
    return {"messaggio": "Funzionalità manutenzioni non ancora implementata"}

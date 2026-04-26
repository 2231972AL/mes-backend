from fastapi import APIRouter

router = APIRouter(prefix="/notifiche", tags=["Notifiche"])

# Router disattivato perché il modello Notifica non esiste
# e il modulo originale era incompleto.
# Quando avrai un modello Notifica reale, potremo riattivarlo.

@router.get("/")
def notifiche_placeholder():
    return {"messaggio": "Funzionalità notifiche non ancora implementata"}

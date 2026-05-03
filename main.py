from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# Database
# -------------------------------
from database import Base, engine
from models import Utente  # importa almeno un modello per creare le tabelle

# Crea tutte le tabelle nel database
Base.metadata.create_all(bind=engine)

# -------------------------------
# Routers
# -------------------------------
from routers import (
    users,
    login,
    commesse,
    fasi,
    log,
    operatori,
    timer,
    materiali,
    lotti,
    gantt,
    notifiche,
    kpi,
    manutenzioni
)

# -------------------------------
# App FastAPI
# -------------------------------
app = FastAPI(
    title="MES Backend",
    version="1.0.0"
)

# -------------------------------
# CORS
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include Routers
# -------------------------------
app.include_router(users.router)
app.include_router(login.router)
app.include_router(commesse.router)
app.include_router(fasi.router)
app.include_router(log.router)
app.include_router(operatori.router)
app.include_router(timer.router)
app.include_router(materiali.router)
app.include_router(lotti.router)
app.include_router(gantt.router)
app.include_router(notifiche.router)
app.include_router(kpi.router)
app.include_router(manutenzioni.router)

# -------------------------------
# Avvio server
# -------------------------------
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)

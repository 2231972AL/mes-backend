from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import Base, engine
from routers import (
    login,
    commesse,
    fasi,
    timer,
    materiali,
    lotti,
    gantt,
    notifiche,
    qualita,
    manutenzione,
    kpi,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="MES Officina")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS] if settings.CORS_ORIGINS != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(commesse.router)
app.include_router(fasi.router)
app.include_router(timer.router)
app.include_router(materiali.router)
app.include_router(lotti.router)
app.include_router(gantt.router)
app.include_router(notifiche.router)
app.include_router(qualita.router)
app.include_router(manutenzione.router)
app.include_router(kpi.router)

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Utente(Base):
    __tablename__ = "utenti"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    attivo = Column(Integer, default=1)

    commesse = relationship("Commessa", back_populates="operatore")
    log = relationship("LogLavorazione", back_populates="operatore")


class Commessa(Base):
    __tablename__ = "commesse"

    id = Column(Integer, primary_key=True, index=True)
    codice = Column(String(50), unique=True, nullable=False)
    descrizione = Column(String(200), nullable=True)

    stato = Column(String(30), default="in_attesa")
    operatore_id = Column(Integer, ForeignKey("utenti.id"), nullable=True)

    ora_inizio = Column(DateTime, nullable=True)
    ora_fine = Column(DateTime, nullable=True)

    note = Column(String(200), nullable=True)

    operatore = relationship("Utente", back_populates="commesse")
    fasi = relationship("Fase", back_populates="commessa", cascade="all, delete-orphan")
    log = relationship("LogLavorazione", back_populates="commessa", cascade="all, delete-orphan")


class Fase(Base):
    __tablename__ = "fasi"

    id = Column(Integer, primary_key=True, index=True)
    commessa_id = Column(Integer, ForeignKey("commesse.id"))
    nome = Column(String)
    tempo_previsto = Column(Integer)

    stato = Column(String(30), default="da_fare")

    commessa = relationship("Commessa", back_populates="fasi")
    log = relationship("LogLavorazione", back_populates="fase", cascade="all, delete-orphan")


class LogLavorazione(Base):
    __tablename__ = "log_lavorazione"

    id = Column(Integer, primary_key=True, index=True)

    commessa_id = Column(Integer, ForeignKey("commesse.id"), nullable=False)
    fase_id = Column(Integer, ForeignKey("fasi.id"), nullable=True)
    operatore_id = Column(Integer, ForeignKey("utenti.id"), nullable=True)

    azione = Column(String(50), nullable=False)
    minuti = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    commessa = relationship("Commessa", back_populates="log")
    fase = relationship("Fase", back_populates="log")
    operatore = relationship("Utente", back_populates="log")


class Sessione(Base):
    __tablename__ = "sessioni"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utenti.id"))
    token = Column(String(200), unique=True, nullable=False)

    utente = relationship("Utente")
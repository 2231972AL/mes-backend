from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class LoginResponse(BaseModel):
    token: str
    nome: str
    ruolo: str
from pydantic import BaseModel

class LoginRequest(BaseModel):
    pin: str


class CommessaBase(BaseModel):
    id: int
    codice: str
    descrizione: Optional[str]
    stato: str

    class Config:
        orm_mode = True

class FaseBase(BaseModel):
    id: int
    nome: str
    stato: str
    tempo_previsto: int
    tempo_reale: int

    class Config:
        orm_mode = True

class ScartoCreate(BaseModel):
    fase_id: int
    motivo: str
    quantita: int

class MaterialeBase(BaseModel):
    id: int
    nome: str
    spessore: float
    giacenza: int

    class Config:
        orm_mode = True

class LottoBase(BaseModel):
    id: int
    materiale_id: int
    quantita: int
    certificato: str
    created_at: datetime

    class Config:
        orm_mode = True

class NotificaBase(BaseModel):
    id: int
    tipo: str
    messaggio: str
    livello: str
    letta: bool
    created_at: datetime

    class Config:
        orm_mode = True


# -------------------------
# AGGIUNGI QUESTE DUE CLASSI
# -------------------------

class UserCreate(BaseModel):
    nome: str
    pin: str
    ruolo: str = "operatore"


class UserLogin(BaseModel):
    nome: str
    pin: str
class OperatorBase(BaseModel):
    name: str
    pin: str


class OperatorCreate(OperatorBase):
    pass


class Operator(OperatorBase):
    id: int

    class Config:
        orm_mode = True
from pydantic import BaseModel

class OperatorBase(BaseModel):
    name: str
    pin: str

class OperatorCreate(OperatorBase):
    pass

class Operator(OperatorBase):
    id: int

    class Config:
        from_attributes = True

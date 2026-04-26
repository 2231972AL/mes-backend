from sqlalchemy.orm import Session
import models, schemas


# -----------------------------
# OPERATORS
# -----------------------------

def create_operator(db: Session, operator: schemas.OperatorCreate):
    db_operator = models.Operator(
        name=operator.name,
        pin=operator.pin
    )
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


def get_operator_by_pin(db: Session, pin: str):
    return db.query(models.Operator).filter(models.Operator.pin == pin).first()
from sqlalchemy.orm import Session
import models, schemas


# -----------------------------
# OPERATORS
# -----------------------------

def create_operator(db: Session, operator: schemas.OperatorCreate):
    db_operator = models.Operator(
        name=operator.name,
        pin=operator.pin
    )
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


def get_operator_by_pin(db: Session, pin: str):
    return db.query(models.Operator).filter(models.Operator.pin == pin).first()
from sqlalchemy.orm import Session
import models, schemas


# -----------------------------
# OPERATORS
# -----------------------------

def create_operator(db: Session, operator: schemas.OperatorCreate):
    db_operator = models.Operator(
        name=operator.name,
        pin=operator.pin
    )
    db.add(db_operator)
    db.commit()
    db.refresh(db_operator)
    return db_operator


def get_operator_by_pin(db: Session, pin: str):
    return db.query(models.Operator).filter(models.Operator.pin == pin).first()

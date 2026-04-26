from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import schemas, crud
from database import get_db

router = APIRouter(prefix="/operators", tags=["operators"])


@router.post("/", response_model=schemas.Operator)
def create_operator(operator: schemas.OperatorCreate, db: Session = Depends(get_db)):
    return crud.create_operator(db, operator)


@router.get("/", response_model=list[schemas.Operator])
def get_operators(db: Session = Depends(get_db)):
    return db.query(crud.models.Operator).all()


@router.post("/login")
def login(pin: str, db: Session = Depends(get_db)):
    op = crud.get_operator_by_pin(db, pin)
    if not op:
        return {"success": False}
    return {"success": True, "operator": op}

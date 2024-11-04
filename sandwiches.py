# api/controllers/sandwiches.py
from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.models import Sandwich  # Import your Sandwich model
from api.schemas import SandwichCreate, SandwichUpdate, SandwichResponse  # Import your schemas

router = APIRouter()

@router.post("/", response_model=SandwichResponse)
def create_sandwich(sandwich: SandwichCreate, db: Session = Depends(get_db)):
    db_sandwich = Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

@router.get("/", response_model=list[SandwichResponse])
def read_all_sandwiches(db: Session = Depends(get_db)):
    return db.query(Sandwich).all()

@router.get("/{sandwich_id}", response_model=SandwichResponse)
def read_one_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    return sandwich

@router.put("/{sandwich_id}", response_model=SandwichResponse)
def update_sandwich(sandwich_id: int, sandwich: SandwichUpdate, db: Session = Depends(get_db)):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    for key, value in sandwich.dict(exclude_unset=True).items():
        setattr(db_sandwich, key, value)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

@router.delete("/{sandwich_id}", response_model=SandwichResponse)
def delete_sandwich(sandwich_id: int, db: Session = Depends(get_db)):
    db_sandwich = db.query(Sandwich).filter(Sandwich.id == sandwich_id).first()
    if db_sandwich is None:
        raise HTTPException(status_code=404, detail="Sandwich not found")
    db.delete(db_sandwich)
    db.commit()
    return db_sandwich

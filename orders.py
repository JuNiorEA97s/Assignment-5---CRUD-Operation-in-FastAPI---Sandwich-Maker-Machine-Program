from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas

def create_order(db: Session, order: schemas.OrderCreate):
    # Create a new instance of the Order model with the provided data
    db_order = models.Order(
        customer_name=order.customer_name,
        description=order.description
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_all_orders(db: Session):
    return db.query(models.Order).all()

def get_order(db: Session, order_id: int):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    db_order = get_order(db, order_id)
    update_data = order.dict(exclude_unset=True)  # Use .dict() for Pydantic models
    for key, value in update_data.items():
        setattr(db_order, key, value)  # Update attributes dynamically
    db.commit()
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    db.delete(db_order)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import models, schemas
from app.auth import get_current_user, get_admin_user
from app.database import get_db
from datetime import datetime,timezone
router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(
    skip: int = 0,
    limit: int = 10,
    client_id: Optional[int] = None,
    status: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):

    query = db.query(models.Order)
    if client_id:
        query = query.filter(models.Order.client_id == client_id)
    if status:
        query = query.filter(models.Order.status.ilike(status))
    if start_date:
        query = query.filter(models.Order.date >= start_date)
    if end_date:
        query = query.filter(models.Order.date <= end_date)

    return query.offset(skip).limit(limit).all()


@router.get("/{order_id}", response_model=schemas.OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order


@router.post("/", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    # Valida stock
    for item in order.products:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produto {item.product_id} não encontrado")
        if product.actual_stock < item.amount:
            raise HTTPException(status_code=400, detail=f"Estoque insuficiente para o produto {product.id}")

    new_order = models.Order(
        client_id=current_user.id,
        name=order.name,
        status=order.status,
    )
    db.add(new_order)
    db.flush()  # gera ID

    for item in order.products:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        product.actual_stock -= item.amount
        db.add(models.ProductOrder(order_id=new_order.id, product_id=product.id, amount=item.amount))

    db.commit()
    db.refresh(new_order)
    return new_order


@router.put("/{order_id}", response_model=schemas.OrderRead)
def update_order(order_id: int, order_data: schemas.OrderUpdate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    if order_data.status:
        order.status = order_data.status
    if order_data.name:
        order.name = order_data.name
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db), current_user: models.Client = Depends(get_admin_user)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    db.delete(order)
    db.commit()
    return {"detail": "Pedido deletado com sucesso"}


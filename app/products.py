from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import database, models, schemas
from app.auth import get_current_user, get_admin_user
from sqlalchemy.exc import IntegrityError
from app.database import get_db
router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(
    skip: int = 0,
    limit: int = 10,
    section: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
    current_user: models.Client = Depends(get_current_user)
):
    query = db.query(models.Product)

    if section:
        query = query.filter(models.Product.section.ilike(f"%{section}%"))
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Product.sale_price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.sale_price <= max_price)

    return query.offset(skip).limit(limit).all()


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return product


@router.post("/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    new_product = models.Product(**product.dict())
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        return new_product
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Erro ao criar produto")


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, product_data: schemas.ProductCreate, db: Session = Depends(get_db), current_user: models.Client = Depends(get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: models.Client = Depends(get_admin_user)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}


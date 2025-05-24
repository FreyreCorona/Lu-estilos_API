from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.schemas import ClientRead,ClientCreate
from app.models import Client
from app.auth import get_admin_user,get_current_user 

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=List[ClientRead])
def list_clients(
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Client = Depends(get_current_user)
):
    query = db.query(Client)
    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))
    return query.offset(skip).limit(limit).all()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db), current_user: Client = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return client


@router.post("/", response_model=ClientRead)
def create_client(client: ClientCreate, db: Session = Depends(get_db), current_user: Client = Depends(get_current_user)):
    new_client = Client(**client.dict())
    try:
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email ou CPF já cadastrado")


@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db), current_user: Client = Depends(get_current_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    for key, value in client_data.dict().items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db), current_user: Client = Depends(get_admin_user)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(client)
    db.commit()
    return {"detail": "Cliente deletado com sucesso"}


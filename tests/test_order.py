import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app
from app import models
from datetime import datetime,timezone
from app.database import session_local
from sqlalchemy.orm import Session

@pytest.mark.asyncio
async def test_full_order_crud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Registrar e logar admin
        await ac.post("/auth/register", json={
            "name": "Admin",
            "email": "admin3@example.com",
            "cpf": "11122233399",
            "role": "admin",
            "password": "adminpass"
        })
        db:Session = session_local()
        admin = db.query(models.Client).filter_by(email="admin3@example.com").first()
        admin.role = "admin"
        db.commit()
        db.close()

        login = await ac.post("/auth/login", json={
            "email": "admin3@example.com",
            "password": "adminpass"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Criar produto
        product = await ac.post("/products/", json={
            "name":"producto",
            "description": "Vestido",
            "section": "feminino",
            "code_bar": "8887776661234",
            "category": "vestidos",
            "initial_stock": 10,
            "actual_stock": 10,
            "due_date": f"{datetime.now(timezone.utc)}",
            "price": 89.90,
        }, headers=headers)
        product_id = product.json()["id"]
        
        response= await ac.get(f"/clients/", headers=headers)
        client_id = response.json()[0]['id']
        # POST /orders
        create = await ac.post("/orders/", json={
            
            "name": "order 1",
            "status": "pending",
            "client_id" : client_id,
            "products": [{"product_id": product_id, "amount": 2,"order_id": 1}]
        }, headers=headers)
        assert create.status_code == 200
        order_id = create.json()["id"]

        # GET /orders
        get = await ac.get("/orders/", headers=headers)
        assert get.status_code == 200
        assert len(get.json()) > 0

        # GET /orders/{id}
        detail = await ac.get(f"/orders/{order_id}", headers=headers)
        assert detail.status_code == 200
        assert detail.json()["id"] == order_id

        # PUT /orders/{id}
        update = await ac.put(f"/orders/{order_id}", json={"status": "enviado"}, headers=headers)
        assert update.status_code == 200
        assert update.json()["status"] == "enviado"

        # DELETE /orders/{id}
        delete = await ac.delete(f"/orders/{order_id}", headers=headers)
        assert delete.status_code == 200


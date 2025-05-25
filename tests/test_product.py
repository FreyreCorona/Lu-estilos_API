import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app
from app import models
from app.database import session_local
from datetime import datetime,timezone
from sqlalchemy.orm import Session

@pytest.mark.asyncio
async def test_full_product_crud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # Registrar e logar admin
        await ac.post("/auth/register", json={
            "name": "Admin",
            "email": "admin2@example.com",
            "cpf": "99988877766",
            "role": "user",
            "password": "adminpass"
        })
        db:Session = session_local()
        admin = db.query(models.Client).filter_by(email="admin2@example.com").first()
        admin.role = "admin"
        db.commit()
        db.close()

        login = await ac.post("/auth/login", json={
            "email": "admin2@example.com",
            "password": "adminpass"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # POST /products
        create = await ac.post("/products/", json={
            "name": "producto 1",
            "description": "Tênis",
            "section": "calçados",
            "code_bar": "1234567890123",
            "categroy": "esportivo",
            "initial_stock": 15,
            "actual_stock": 15,
            "due_date": f"{datetime.now(timezone.utc)}",
            "category": "esportivo",
            "price": 4000.50,
        }, headers=headers)
        assert create.status_code == 200
        product_id = create.json()["id"]

        # GET /products
        response = await ac.get("/products/", headers=headers)
        assert response.status_code == 200
        assert len(response.json()) > 0

        # GET /products/{id}
        single = await ac.get(f"/products/{product_id}", headers=headers)
        assert single.status_code == 200
        assert single.json()["description"] == "Tênis"

        # PUT /products/{id}
        update = await ac.put(f"/products/{product_id}", headers=headers, json={
            "name":"prducto 1",
            "description": "Tênis atualizado",
            "section": "calçados",
            "code_bar": "1234567890123",
            "category": "casual",
            "initial_stock": 15,
            "actual_stock": 10,
            "due_date": f"{datetime.now(timezone.utc)}",
            "price": 219.90,
        })
        assert update.status_code == 200
        assert update.json()["description"] == "Tênis atualizado"

        # DELETE /products/{id}
        delete = await ac.delete(f"/products/{product_id}", headers=headers)
        assert delete.status_code == 200


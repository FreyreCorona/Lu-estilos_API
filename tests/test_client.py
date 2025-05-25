import pytest
from httpx import AsyncClient,ASGITransport
from app.main import app
from app import models
from app.database import session_local
from sqlalchemy.orm import Session
from random import choice

@pytest.mark.asyncio
async def test_full_client_crud():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        rnd_email = f"client{str(choice([10,99]))}@example.com"
        # Cadastar cliente
        register_response = await ac.post("/auth/register", json={
            "name": "Test Client",
            "email": "emailprueba@prueba.com",
            "cpf": f"{str(choice([1000000000,999999999]))}",
            "role": "user",
            "password": "clientpass"
        })
        assert register_response.status_code == 200

        # Login
        login = await ac.post("/auth/login", json={
            "email": "emailprueba@prueba.com",
            "password": "clientpass"
        })
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # GET /clients
        response = await ac.get("/clients/", headers=headers)
        assert response.status_code == 200
        clients = response.json()
        assert len(clients) > 0
        client_id = clients[0]["id"]

        # GET /clients/{id}
        response = await ac.get(f"/clients/{client_id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["email"] == "emailprueba@prueba.com"

        # PUT /clients/{id}
        update = await ac.put(f"/clients/{client_id}", headers=headers, json={
            "name": "Updated Client",
            "email":"emailprueba@prueba.com",
            "cpf": f"{str(choice([1000000000,999999999]))}",
            "role": "user",
            "password": "clientpass"
        })
        assert update.status_code == 200
        assert update.json()["name"] == "Updated Client"
        # DELETE /clients/{id} (requer admin)
        # Criamos admin pra isso
        rnd_email = f"client{str(choice([10,99]))}@example.com",
        await ac.post("/auth/register", json={
            "name": "Admin",
            "email": "adminprueba@prueba.com",
            "cpf": f"{str(choice([1000000000,999999999]))}",
            "role": "user",
            "password": "adminpass"
        })
        await ac.post("/auth/login", json={
            "email": rnd_email,
            "password": "adminpass"
        })
        # Forzar admin na DB o teste manual
        db:Session = session_local()
        admin = db.query(models.Client).filter_by(email="adminprueba@prueba.com").first()
        admin.role = "admin"
        db.commit()
        db.close()

        login_admin = await ac.post("/auth/login", json={
            "email": "adminprueba@prueba.com",
            "password": "adminpass"
        })
        admin_token = login_admin.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}

        delete = await ac.delete(f"/clients/{client_id}", headers=admin_headers)
        assert delete.status_code == 200

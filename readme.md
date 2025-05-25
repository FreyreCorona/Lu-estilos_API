
# Lu-estilos_API

**Lu-estilos_API** is a RESTful API developed with FastAPI that implements CRUD operations for fashion style management. This project showcases the use of modern technologies and best practices in backend development.

---

# Technologies Used

- **FastAPI**: Modern and high-performance framework for building APIs with Python.
- **SQLAlchemy**: ORM for interacting with relational databases.
- **Alembic**: Migration tool for SQLAlchemy.
- **Docker & Docker Compose**: Containerization and service orchestration.
- **Pytest**: Testing framework for Python.
- **PostgreSQL**: Relational database management system.

---

# Project Structure

```bash
Lu-estilos_API/
 app/
 main.py            # Application entry point
 models/            # Data models definitions
 schemas/           # Pydantic schemas
 routers/           # API routes
 services/          # Business logic
 alembic/               # Database migrations
 tests/                 # Unit and integration tests
 docker-compose.yml     # Docker Compose configuration
 Dockerfile             # Docker image definition
 requirements.txt       # Project dependencies
 .env                   # Environment variables (uploaded only for educational proposal)
```

---

## Installation and Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/FreyreCorona/Lu-estilos_API.git
   cd Lu-estilos_API
   ```

2. Copy the `.env` file and set the environment variables as you like

3. Build and start the containers using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Apply database migrations with Alembic:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. Run tests using Pytest:
   ```bash
   docker-compose exec web pytest
   ```

---

##  Tests

The project includes a suite of tests to ensure the functionality and stability of the API. Tests are run using Pytest and cover the main endpoints of the system.

---

## Documentation

FastAPI automatically generates interactive documentation for the API. Once the application is running, you can access:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---


## Contact

Developed by [FreyreCorona](https://github.com/FreyreCorona). If you have any questions or suggestions, feel free to open an issue or contact me directly.


# Lu-estilos_API

**Lu-estilos_API** es una API RESTful desarrollada con FastAPI que implementa operaciones CRUD para la gestiÃ³n de estilos de moda. Este proyecto demuestra el uso de tecnologÃ­as modernas y buenas prÃ¡cticas en el desarrollo backend.

---

## ðŸš€ TecnologÃ­as Utilizadas

- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs con Python.
- **SQLAlchemy**: ORM para la interacciÃ³n con bases de datos relacionales.
- **Alembic**: Herramienta de migraciones para SQLAlchemy.
- **Docker & Docker Compose**: ContenerizaciÃ³n y orquestaciÃ³n de servicios.
- **Pytest**: Framework de pruebas para Python.
- **PostgreSQL**: Sistema de gestiÃ³n de bases de datos relacional.

---

## ðŸ› ï¸ Estructura del Proyecto

```bash
Lu-estilos_API/
â”œâ”€â”€ app/
â”‚   â”œâ”€â”€ main.py            # Punto de entrada de la aplicaciÃ³n
â”‚   â”œâ”€â”€ models/            # DefiniciÃ³n de modelos de datos
â”‚   â”œâ”€â”€ schemas/           # Esquemas de Pydantic
â”‚   â”œâ”€â”€ routers/           # Rutas de la API
â”‚   â””â”€â”€ services/          # LÃ³gica de negocio
â”œâ”€â”€ alembic/               # Migraciones de base de datos
â”œâ”€â”€ tests/                 # Pruebas unitarias y de integraciÃ³n
â”œâ”€â”€ docker-compose.yml     # ConfiguraciÃ³n de Docker Compose
â”œâ”€â”€ Dockerfile             # DefiniciÃ³n de la imagen Docker
â”œâ”€â”€ requirements.txt       # Dependencias del proyecto
â””â”€â”€ .env                   # Variables de entorno
```

---

## ðŸ“¦ InstalaciÃ³n y EjecuciÃ³n Local

1. Clona el repositorio:
   ```bash
   git clone https://github.com/FreyreCorona/Lu-estilos_API.git
   cd Lu-estilos_API
   ```

2. Copia el archivo `.env` con las variables de entorno necesarias.

3. Construye y levanta los contenedores con Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Aplica las migraciones de la base de datos con Alembic:
   ```bash
   docker-compose exec web alembic upgrade head
   ```

5. Ejecuta las pruebas con Pytest:
   ```bash
   docker-compose exec web pytest
   ```

---

## ðŸ§ª Pruebas

El proyecto incluye un conjunto de pruebas para garantizar la funcionalidad y estabilidad de la API. Las pruebas se ejecutan utilizando Pytest y cubren los endpoints principales del sistema.

---

## ðŸ“„ DocumentaciÃ³n

FastAPI genera automÃ¡ticamente documentaciÃ³n interactiva para la API. Una vez que la aplicaciÃ³n estÃ© en ejecuciÃ³n, puedes acceder a la documentaciÃ³n en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## ðŸ¤ Contribuciones

Â¡Las contribuciones son bienvenidas! Si deseas mejorar este proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commits (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a la rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

---

## ðŸ“¬ Contacto

Desarrollado por [FreyreCorona](https://github.com/FreyreCorona). Si tienes alguna pregunta o sugerencia, no dudes en abrir un issue o contactarme directamente.

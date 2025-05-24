from fastapi import FastAPI
from app import auth,client,products
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.include_router(auth.router)
app.include_router(client.router)
app.include_router(products.router)

@app.get('/')
async def read_root():
    return {"msg": "Lu Api"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Lu Estilo API",
        version="1.0.0",
        description="API com autenticação JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

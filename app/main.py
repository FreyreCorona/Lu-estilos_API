from fastapi import FastAPI
from app import auth

app = FastAPI()

app.include_router(auth.router)

@app.get('/')
async def read_root():
    return {"msg": "Lu Api"}



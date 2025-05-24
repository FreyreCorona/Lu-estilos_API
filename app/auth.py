from datetime import timedelta,datetime,timezone
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
from app.schemas import ClientCreate, ClientLogin,Token
from app.models import Client
from app.database import get_db

load_dotenv()
router = APIRouter(prefix='/auth',tags=['auth'])
JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain,hashed):
    return bcrypt_context.verify(plain,hashed)

def get_password_hash(password):
    return bcrypt_context.hash(password)

def create_access_token(data:dict,expires_delta:timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=ALGORITHM)

def decode_token(token:str):
    return jwt.decode(token,JWT_SECRET_KEY,algorithms=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_email = payload.get("sub")
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(Client).filter(Client.email == user_email).first()
    if user is None:
        raise credentials_exception
    return user

def get_admin_user(current_user: Client = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem executar esta ação")
    return current_user

@router.post('/register',response_model=Token)
def register(user:ClientCreate,db:Session = Depends(get_db)):
    db_user = db.query(Client).filter(Client.email == user.email or Client.cpf == user.cpf).first()
    if db_user:
        raise HTTPException(status_code=400,detail="Esse usuario ja existe")
    hashed_password = get_password_hash(user.password)
    new_user = Client(name=user.name,email = user.email,password=hashed_password,cpf=user.cpf,role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token(data={"sub":new_user.email})
    return {"access_token": token,"token_type":"bearer"}

@router.post("/login",response_model=Token)
def login(user:ClientLogin,db:Session = Depends(get_db)):
    db_user = db.query(Client).filter(Client.email == user.email).first()
    if not db_user or not verify_password(user.password,db_user.password):
        raise HTTPException(status_code=400,detail="User o password incorrectos")
    token = create_access_token(data={"sub":db_user.email})
    return {"access_token":token,"token_type":"bearer"}


@router.post("/refresh-token",response_model=Token)
def refresh_token(token:Token):
    try:
        payload = decode_token(token.access_token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401,detail="Token invalido")
        new_token = create_access_token(data={"sub":email})
        return {"access_token":new_token,"token_type":"bearer"}
    except Exception:
        raise HTTPException(status_code=401,detail="Token invalido o expirado")

import bcrypt
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

from src.common.functions import timezone_br
from src.configurations import Configurations

configurations = Configurations()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/customers/login")

def normal_user_required(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, configurations.SECRET_KEY, algorithms=[configurations.ALGORITHM])
        return {"id": payload.get("sub"), "role": payload.get("role")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone_br()) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, configurations.SECRET_KEY, algorithm=configurations.ALGORITHM)

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

def admin_required(user = Depends(normal_user_required)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return user
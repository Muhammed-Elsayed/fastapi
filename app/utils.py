import datetime
from datetime import timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from app.models import models as models
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db
from sqlalchemy.orm import Session


SECRET_KEY = "1e0788a28e2e503315a3a894d353abaa36ace075faae8650f714d7c880f01da5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_token(payload: dict, duration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    payload["exp"] = datetime.datetime.now() + timedelta(minutes=duration)
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Admin:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin_instance = db.query(models.Admin).filter(models.Admin.email == email).first()
    # print(admin_instance)
    if not isinstance(admin_instance, models.Admin):
        raise credentials_exception
    return admin_instance

# def decode_token(token):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
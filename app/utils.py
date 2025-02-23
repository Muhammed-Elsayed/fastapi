import datetime
from datetime import timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from app.models import models as models
from fastapi.security import OAuth2PasswordBearer
from app.db.database import get_db
from sqlalchemy.orm import Session


# Strong Secret key used to sign JWT tokens with the Algorithm below 
SECRET_KEY = "1e0788a28e2e503315a3a894d353abaa36ace075faae8650f714d7c880f01da5"

# Algorithm used for JWT encoding/decoding
ALGORITHM = "HS256"

# Token expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 1

# OAuth2 scheme for extracting the token from requests (typically from the Authorization header)
# it extracts tokens from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")   # this tokenUR is just for documentation


def create_token(payload: dict, duration: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """
    Creates a JWT token with the given payload and expiration time.
    
    Args:
        payload (dict): The data to be included in the token.
        duration (int): Expiration time in minutes (default is 30 minutes).
    
    Returns:
        str: Encoded JWT token.
    """
    # Add expiration time to the token payload
    payload["exp"] = datetime.datetime.now() + timedelta(minutes=duration)
    
    # Encode the payload using the secret key and return the JWT token
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.Admin:
    """
    Extracts and verifies the current user from the JWT token.
    
    Args:
        token (str): JWT token extracted from the request.
        db (Session): Database session dependency.
    
    Returns:
        models.Admin: The authenticated admin user instance.
    
    Raises:
        HTTPException: If authentication fails (invalid or expired token).
    """
    # Exception to be raised if authentication fails
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Decode the token and extract the payload
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Extract the email from the payload
        email = payload.get("email")
        
        # If email is missing in the payload, raise an authentication error
        if email is None:
            raise credentials_exception
    
    except JWTError:
        # Raised if decoding fails (invalid token, expired, or tampered)
        raise credentials_exception

    # Query the database to find the admin user by email
    admin_instance = db.query(models.Admin).filter(models.Admin.email == email).first()
    
    # print(admin_instance)  # Debugging line to check the retrieved admin object

    # Ensure that the retrieved object is an instance of the Admin model
    if not isinstance(admin_instance, models.Admin):
        raise credentials_exception

    return admin_instance  # Return the authenticated admin user

# def decode_token(token):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
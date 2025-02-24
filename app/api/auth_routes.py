from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Admin
from app.schemas.auth_schema import AdminCreate, AdminResponse, LoginRequest
from app.crud.auth_crud import get_admin_by_email, create_admin
from app.db.database import get_db
from app.utils import create_token, get_current_user
router = APIRouter()



@router.post("/create_admin", response_model=AdminResponse)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    existing_admin = get_admin_by_email(db, admin.email)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_admin = create_admin(db, admin)
    return new_admin



@router.post("/login")
async def signin(login_request: LoginRequest, db: Session = Depends(get_db)):
    admin = get_admin_by_email(db, login_request.email)
    print(admin)
    if admin:
        if admin.verify_password(login_request.password):
            token = create_token({"email": login_request.email, "password": login_request.password})
            
            # Set token as an HTTPOnly cookie (adjust options as needed)
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                secure=True,       # set to True in production with HTTPS
                samesite="lax"     # adjust samesite as needed (e.g., 'strict')
            )
            
            # Also return the token in the body
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect password")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="user not found")  # for debugging only, should be changed to raise unauthorized always


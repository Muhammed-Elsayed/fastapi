from sqlalchemy.orm import Session
from app.models.models import Admin
from app.schemas.auth_schema import AdminCreate, AdminResponse


def get_admin_by_email(db: Session, email: str):
    return db.query(Admin).filter(Admin.email == email).first()


def create_admin(db: Session, admin_data: AdminCreate):
    new_admin = Admin(
        name=admin_data.name,
        email=admin_data.email,
        join_date=admin_data.join_date
    )
    new_admin.set_password(admin_data.password)  # Hash the password
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return new_admin
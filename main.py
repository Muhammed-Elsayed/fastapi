from fastapi import FastAPI
from app.api import employee_routes, auth_routes
from app.db.database import Base, engine, SessionLocal

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(employee_routes.router, tags=["employees"])
app.include_router(auth_routes.router, tags=["Admin"])

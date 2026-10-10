from app.core.database import engine, Base
from app.models.job import Job
from app.models.application import Application

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")

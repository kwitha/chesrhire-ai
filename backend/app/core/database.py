from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session


DATABASE_URL = "postgresql+psycopg://chesrhire_user:root@localhost:5432/chesrhire_db"


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


class Base(DeclarativeBase):
    pass


def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()


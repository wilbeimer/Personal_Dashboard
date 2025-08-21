# create_db.py
from app.database import Base, engine
from app.models import User


def create_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_db()

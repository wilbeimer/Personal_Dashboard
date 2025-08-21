# tests/test_crud.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.crud import create_user, get_user_by_email
from app.database import Base
from app.models import User
from app.schemas import UserCreate

# Setup a temporary SQLite DB for testing
TEST_DATABASE_URL = "sqlite:///./tests/test_dashboard.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture
def db_session():
    # Create tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


def test_create_and_fetch_user(db_session):
    # Create a test user
    user_in = UserCreate(email="test@example.com", password="password123")
    user = create_user(db_session, user_in)

    assert user.id is not None
    assert user.email == "test@example.com"

    # Fetch the same user
    fetched_user = get_user_by_email(db_session, "test@example.com")
    assert fetched_user.id == user.id
    assert fetched_user.email == user.email

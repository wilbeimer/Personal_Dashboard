from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import Note, User
from app.schemas import NoteCreate, UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --------------------
# User operations
# --------------------


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def create_user(db: Session, user: UserCreate) -> User:
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, password_hash=hashed_pw)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def delete_all_users(db: Session):
    db.query(User).delete()
    db.commit()


# --------------------
# Note operations
# --------------------


def create_note_for_user(db: Session, user_id: int, note: NoteCreate) -> Note:
    db_note = Note(title=note.title, content=note.content, user_id=user_id)

    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    print(db_note.id)
    return db_note


def get_notes_for_user(db: Session, user_id: int) -> list[Note]:
    return (
        db.query(Note)
        .filter(Note.user_id == user_id)
        .order_by(Note.created_at.desc())
        .all()
    )


def get_note_by_id(db: Session, note_id: int) -> Note | None:
    return db.query(Note).filter(Note.id == note_id).first()


def update_note_for_user(note: NoteCreate, db_note: Note, db: Session) -> Note:
    db_note.title = note.title
    db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note_by_id(db: Session, note_id: int):
    db.query(Note).filter(Note.id == note_id).first().delete()
    db.commit()

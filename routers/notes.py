from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.crud import (create_note_for_user, delete_note_by_id, get_note_by_id,
                      get_notes_for_user, update_note_for_user)
from app.database import get_db
from app.models import User
from app.schemas import NoteCreate, NoteOut

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[NoteOut], status_code=200)
def get_notes(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    notes = get_notes_for_user(db=db, user_id=current_user.id)
    return notes


@router.post("/", response_model=NoteOut, status_code=201)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_note = create_note_for_user(note=note, user_id=current_user.id, db=db)
    return new_note


@router.put("/{id}", response_model=NoteOut)
def update_note(
    id: int,
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Fetch note
    db_note = get_note_by_id(db, id)
    if not db_note or db_note.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Note not found")

    # Update note
    updated_note = update_note_for_user(note=note, db_note=db_note, db=db)
    return updated_note


@router.delete("/{id}", response_model=NoteOut, status_code=200)
def delete_note(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_note = delete_note_by_id(note_id=id, db=db, user_id=current_user.id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return deleted_note

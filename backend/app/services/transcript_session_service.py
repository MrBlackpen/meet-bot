# backend/app/services/transcript_session_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.db.models import TranscriptSession


def get_or_create_session(db: Session, session_id: str):
    """
    Idempotently ensure a TranscriptSession row exists.

    This is written to be safe under concurrent access from multiple
    /append and /finalize calls that may race to create the same session_id.
    """
    # Fast path: most of the time the row already exists
    session = db.query(TranscriptSession).filter_by(session_id=session_id).first()
    if session:
        return session

    # Slow path: try to create, but handle race where another request
    # created the same session_id between our SELECT and COMMIT.
    session = TranscriptSession(session_id=session_id)
    db.add(session)

    try:
        db.commit()
    except IntegrityError:
        # Another transaction won the race; discard our pending insert
        db.rollback()
        session = (
            db.query(TranscriptSession)
            .filter_by(session_id=session_id)
            .first()
        )
        if not session:
            # Should not normally happen, but fall back to raising
            raise
    else:
        db.refresh(session)

    return session


def finalize_session(db: Session, session_id: str):
    session = get_or_create_session(db, session_id)

    if session.is_finalized:
        return False  # already finalized

    session.is_finalized = True
    session.finalized_at = datetime.utcnow()
    db.commit()
    return True


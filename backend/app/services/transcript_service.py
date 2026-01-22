# backend/app/services/transcript_service.py
import os
from threading import Lock

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TRANSCRIPT_DIR = os.path.join(BASE_DIR, "transcripts")
os.makedirs(TRANSCRIPT_DIR, exist_ok=True)

# Simple per-process file lock map
_file_locks = {}


def _get_lock(session_id: str) -> Lock:
    if session_id not in _file_locks:
        _file_locks[session_id] = Lock()
    return _file_locks[session_id]


def get_transcript_path(session_id: str) -> str:
    return os.path.join(TRANSCRIPT_DIR, f"meet_{session_id}.txt")


def append_line(session_id: str, line: str):
    path = get_transcript_path(session_id)
    lock = _get_lock(session_id)

    with lock:
        with open(path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_full_transcript(session_id: str) -> str:
    path = get_transcript_path(session_id)
    if not os.path.exists(path):
        raise FileNotFoundError("Transcript file not found")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()

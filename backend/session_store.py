import uuid

_sessions = {}

def create_session(code: str) -> str:
    session_id = str(uuid.uuid4())
    _sessions[session_id] = code
    return session_id

def get_code(session_id: str) -> str:
    return _sessions.get(session_id, "")

def update_code(session_id: str, code: str):
    _sessions[session_id] = code

import os
from functools import wraps
from scbt.session import session

actions = dict()

def action(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    actions[f.__name__] = f
    return wrapper

@action
def add_torrent(payload):
    path = payload.get("path")
    if not path:
        return { "success": False, "error": "'path' is required" }
    if not os.path.exists(path):
        return { "success": False, "error": "File not found" }
    h, t = session.add_torrent(path)
    return { "success": True, "info_hash": h }

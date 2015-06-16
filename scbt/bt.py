import libtorrent as lt
import binascii
from scbt.config import _cfg
from scbt.actions import actions

def execute(payload):
    action = payload.get("action")
    if not action:
        return "Unknown action '{}'\n".format(action)
    return action(payload)

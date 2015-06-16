import asyncio
import json
from scbt.config import _cfg
from scbt.protocol import SCBTOneOffClient

@asyncio.coroutine
def wait(c, future):
    asyncio.async(c)
    result = yield from future
    return result

def send_command(cmd):
    if "\n" not in cmd:
        cmd += "\n"
    loop = asyncio.get_event_loop()
    ep = _cfg("listen", "ep")
    future = asyncio.Future()
    client = SCBTOneOffClient(cmd, future=future)
    if ep.startswith("unix://"):
        path = ep[len("unix://"):]
        c = loop.create_unix_connection(lambda: client, path=path)
    elif ep.startswith("tcp://"):
        parts = ep[len("tcp://"):].split(":")
        iface = parts[0]
        if len(parts) > 1:
            port = int(parts[1])
        else:
            port = 50932
        c = loop.create_connection(lambda: client, iface, port)
    return loop.run_until_complete(wait(c, future))

def send_action(action, payload={}):
    payload["action"] = action
    return json.loads(send_command(json.dumps(payload)))

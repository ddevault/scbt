import libtorrent as lt
import binascii
from scbt.config import _cfg
from scbt.session import session

commands = dict()

def execute(command):
    cmd = commands.get(command[0])
    if not cmd:
        return "Error: unknown command\n"
    output = cmd(command[1:])
    if output:
        output += "\n"
    return output

def add_torrent(args):
    if len(args) < 1:
        return "Error: Invalid usage"
    path = args[0]
    h, t = session.add_torrent(path)
    return "Added {}".format(h)
commands["add_torrent"] = add_torrent
commands["add"] = add_torrent

def list_torrents(args):
    # TODO: Allow filtering
    response = "{} torrents".format(len(session.torrents))
    for k, t in session.torrents.items():
        status = t.status()
        info = t.torrent_file()
        state = str(status.state)
        if state == "downloading":
            state += " {:.0f}%".format(status.progress)
        response += "\n{}: {} ({})" \
            .format(k, info.name(), state)
    return response
commands["list_torrents"] = list_torrents
commands["list"] = list_torrents

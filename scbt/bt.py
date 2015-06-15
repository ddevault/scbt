import libtorrent as lt
import binascii
from scbt.config import _cfg

port = int(_cfg("listen", "bt"))
session = lt.session()
session.listen_on(port, port + 10)
# TODO: Configure session settings from config
session.add_extension(lt.create_ut_pex_plugin)
session.add_extension(lt.create_ut_metadata_plugin)
session.add_extension(lt.create_metadata_plugin)
session.set_severity_level(lt.alert.severity_levels.info)

commands = dict()
torrents = dict()

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
    e = lt.bdecode(open(path, 'rb').read())
    info = lt.torrent_info(e)
    params = {
        "save_path": _cfg("torrents", "destination"),
        "storage_mode": lt.storage_mode_t.storage_mode_sparse,
        "ti": info
    }
    t = session.add_torrent(params)
    h = binascii.b2a_hex(info.info_hash().to_bytes()).decode("utf-8")
    torrents[h] = t
    return "Added {}".format(h)
commands["add_torrent"] = add_torrent
commands["add"] = add_torrent

def list_torrents(args):
    # TODO: Allow filtering
    response = "{} torrents".format(len(torrents))
    for k, t in torrents.items():
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

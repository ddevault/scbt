import libtorrent as lt
import binascii
from scbt.config import _cfg
from scbt.logging import log

class Session():
    def __init__(self):
        port = int(_cfg("listen", "bt"))
        self.session = lt.session()
        self.session.listen_on(port, port + 10)
        # TODO: Configure more session settings from config
        self.session.add_extension(lt.create_ut_pex_plugin)
        self.session.add_extension(lt.create_ut_metadata_plugin)
        self.session.add_extension(lt.create_metadata_plugin)
        self.session.set_severity_level(lt.alert.severity_levels.info)

        self.torrents = dict()

    def add_torrent(self, path):
        e = lt.bdecode(open(path, 'rb').read())
        info = lt.torrent_info(e)
        params = {
            "save_path": _cfg("torrents", "destination"),
            "storage_mode": lt.storage_mode_t.storage_mode_sparse,
            "ti": info
        }
        torrent = self.session.add_torrent(params)
        hash = binascii.b2a_hex(info.info_hash().to_bytes()).decode("utf-8")
        self.torrents[hash] = torrent
        log.info("Added torrent {} - {}".format(hash, info.name()))
        return hash, torrent

session = Session()

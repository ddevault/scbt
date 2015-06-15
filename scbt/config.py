import logging
import os
import sys

from configparser import ConfigParser

logger = logging.getLogger("scbt")
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
sh.setFormatter(formatter)

logger.addHandler(sh)

config_paths = ["/etc/scbt.conf", "scbt.conf"]

config = None
for p in config_paths:
    if os.path.exists(p):
        config = ConfigParser()
        config.readfp(open(p))

if not config:
    print("TODO: write default config")
    sys.exit(1)

_cfg = lambda e, k: config.get(e, k)

import os
import sys

from configparser import ConfigParser

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

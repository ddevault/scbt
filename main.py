#!/usr/bin/env python3
import click
import os
import sys
from scbt.logging import log
from scbt.daemon import daemon as _daemon

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        pass # TODO: Default to status

@cli.command(help="Runs the scbt daemon.")
@click.option("--fork", default=False, is_flag=True)
def daemon(fork):
    if fork:
        log.info("Forking to background")
        if os.fork() != 0:
            sys.exit()
    log.info("Running as daemon")
    _daemon()

if __name__ == '__main__':
    cli()

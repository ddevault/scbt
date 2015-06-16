#!/usr/bin/env python3
import click
import os
import sys
from scbt.logging import log
from scbt.daemon import daemon as _daemon
from scbt.client import send_command

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

@cli.command(help="Add a new torrent")
@click.argument('f', type=click.Path(exists=True))
@click.option("--paused", default=False, is_flag=True)
def add(f, paused):
    output = send_command("add {}".format(f))
    sys.stdout.write(output)

if __name__ == '__main__':
    cli()

#!/usr/bin/env python3
import click
import os
import sys
from scbt.logging import log
from scbt.daemon import daemon as _daemon
from scbt.client import send_action

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        status([])

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
    payload = {
        "paused": paused,
        "path": f
    }
    output = send_action("add_torrent", payload)
    if output["success"]:
        sys.stdout.write("Added {}\n".format(output["info_hash"]))
    else:
        sys.stderr.write("Error: {}\n", output["error"])

@cli.command(help="Show status information")
@click.argument('what', nargs=-1)
@click.option('--daemon', default=False, is_flag=True)
def status(what, daemon):
    cwd = os.getcwd()
    # TODO: See if cwd is a download target
    if len(what) == 0:
        # Show general status
        output = send_command("status")
        sys.stdout.write(output)
    else:
        # Show status for what
        pass

if __name__ == '__main__':
    cli()

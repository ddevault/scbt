# scbt

scbt (or "SirCmpwn's BitTorrent") is a bittorrent client daemon. It's designed
to handle your torrents in the background, and you interface with it via the
`scbt` command. It should be easily possible to make fancier frontends, such as
a curses or web interface, when the time comes.

scbt is a work in progress, and is not currently recommended for everyday use.

## Usage

First, run `scbt genconfig` as root. It will create a config file in
`/etc/scbt.conf` for you to edit as you please.

Run this command to start the daemon:

    scbt daemon

It is suggested that you run this through your init system. You can also run it
through your xinitrc or similar:

    scbt daemon --fork

### Add torrents

    $ scbt add example.torrent
    Added 4139bde549fb8a6c41122088e731009ca5eca883

This gives you back an info hash. These are used as what is effectively your
torrent's ID. You can use it again later to query your torrent for status or
modify information about it.

### Status Information

Running `scbt` will tell you the current status of the daemon. If you navigate
to a directory a torrent is downloading in, and run `scbt` again, you'll receive
information about that torrent in particular. You can get the status of a
particular torrent without changing your working directory, too - just run `scbt
[info hash]` or `scbt [download path]`.

### TODO

More commands to come later.

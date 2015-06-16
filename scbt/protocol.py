import asyncio
import shlex
import scbt.bt as bt
from scbt.logging import log

# TODO: Authentication
class SCBTServer(asyncio.Protocol):
    buf = ""

    def connection_made(self, transport):
        self.transport = transport
        log.info("Connection made")

    def data_received(self, data):
        self.buf += data.decode("utf-8")
        while '\n' in self.buf:
            command = self.buf[:self.buf.index('\n')]
            self.buf = self.buf[self.buf.index('\n') + 1:]
            self.execute(shlex.split(command))

    def execute(self, command):
        self.send(bt.execute(command))

    def send(self, s):
        if s:
            self.transport.write(s.encode("utf-8"))
            self.transport.write(b"\x00")

class SCBTClient(asyncio.Protocol):
    buf = ""

    def __init__(self, callback, future = None):
        self.callback = callback
        self.future = future

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.buf += data.decode("utf-8")
        while '\x00' in self.buf:
            text = self.buf[:self.buf.index('\x00')]
            self.buf = self.buf[self.buf.index('\x00') + 1:]
            if self.future:
                self.future.set_result(text)
            callback(self.transport, text)

    def send(self, s):
        if s:
            self.transport.write(s.encode("utf-8"))

class SCBTOneOffClient(asyncio.Protocol):
    buf = ""

    def __init__(self, command, future):
        self.command = command
        self.future = future

    def connection_made(self, transport):
        self.transport = transport
        self.send(self.command)

    def data_received(self, data):
        self.buf += data.decode("utf-8")
        while '\x00' in self.buf:
            text = self.buf[:self.buf.index('\x00')]
            self.buf = self.buf[self.buf.index('\x00') + 1:]
            if self.future:
                self.future.set_result(text)
            self.transport.close()

    def send(self, s):
        if s:
            self.transport.write(s.encode("utf-8"))

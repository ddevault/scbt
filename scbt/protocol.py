import asyncio
import shlex

# TODO: Authentication
class SCBTProtocol(asyncio.Protocol):
    buf = ""

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.buf += data.decode("utf-8")
        while '\n' in self.buf:
            command = self.buf[:self.buf.index('\n')]
            self.buf = self.buf[self.buf.index('\n') + 1:]
            self.execute(shlex.split(command))

    def execute(self, command):
        print("Got command: {}".format(", ".join(command)))
        self.send("Got command: {}".format(", ".join(command)))

    def send(self, s):
        self.transport.write(s.encode("utf-8"))

# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116,W0703,W0201,R0902,R0903,W0613,R0201,E0402


"handler"


import inspect
import queue
import sys
import threading
import time


from .bus import Bus
from .object import Object
from .thread import launch


def __dir__():
    return (
            'Callback',
            'Command',
            'Handler',
            'scan',
           )


__all__ = __dir__()


class Callback(Object):

    cbs = Object()
    errors = []

    def register(self, typ, cbs):
        if typ not in self.cbs:
            setattr(self.cbs, typ, cbs)

    def callback(self, event):
        func = getattr(self.cbs, event.type, None)
        if not func:
            event.ready()
            return
        event.__thr__ = launch(func, event)

    def dispatch(self, event):
        self.callback(event)

    def get(self, typ):
        return getattr(self.cbs, typ)


class Command(Object):

    cmd = Object()
    errors = []

    @staticmethod
    def add(cmd):
        setattr(Command.cmd, cmd.__name__, cmd)

    @staticmethod
    def get(cmd):
        return getattr(Command.cmd, cmd, None)

    @staticmethod
    def handle(evt):
        if not evt.isparsed:
            evt.parse()
        func = Command.get(evt.cmd)
        if func:
            try:
                func(evt)
            except Exception as ex:
                tbk = sys.exc_info()[2]
                evt.__exc__ = ex.with_traceback(tbk)
                Command.errors.append(evt)
                evt.ready()
                return None
            evt.show()
        evt.ready()
        return None

    @staticmethod
    def remove(cmd):
        delattr(Command.cmd, cmd)


class Handler(Callback):

    def __init__(self):
        Callback.__init__(self)
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        self.stopped.clear()
        self.register("event", Command.handle)
        Bus.add(self)

    @staticmethod
    def add(cmd):
        Command.add(cmd)

    def announce(self, txt):
        self.raw(txt)

    def handle(self, event):
        self.dispatch(event)

    def loop(self):
        while not self.stopped.set():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put_nowait(event)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def restart(self):
        self.stop()
        self.start()

    def say(self, channel, txt):
        self.raw(txt)

    def stop(self):
        self.stopped.set()

    def start(self):
        self.stopped.clear()
        self.loop()

    def wait(self):
        while 1:
            time.sleep(1.0)


def scan(mod):
    for key, cmd in inspect.getmembers(mod, inspect.isfunction):
        if key.startswith("cb"):
            continue
        names = cmd.__code__.co_varnames
        if "event" in names:
            Command.add(cmd)

# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:03:39
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 17:01:33
from queue import Queue
from threading import Thread, Event


class WorkerExit(Exception):
    pass


class BaseWorker(object):

    def __init__(self):
        self._mailbox = Queue()
        super(BaseWorker, self).__init__()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is WorkerExit:
            raise WorkerExit()
        return msg

    def close(self):
        self.send(WorkerExit)

    def start(self):
        self._terminated = Event()
        t = Thread(target=self._bootstrap)

        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except WorkerExit:
            pass
        finally:
            self._terminated.set()

    def status(self):
        return self._terminated.is_set()

    def join(self):
        self._terminated.wait()

    def run(self):
        raise NotImplementedError


class Worker(BaseWorker):

    def recv_nowait(self):
        if not self._mailbox.empty():
            msg = self._mailbox.get()
            if msg is WorkerExit:
                raise WorkerExit()
            return msg


if __name__ == '__main__':
    class PrintActor(BaseWorker):

        def run(self):
            while True:
                msg = self.recv()
                print('Got:', msg)
                # raise RuntimeError

    p = PrintActor()
    p.start()
    p.send('Hello')
    p.send('World')
    p.close()
    p.start()
    p.send('Hello')
    p.send('World')
    p.close()
    p.join()

    class TaggedActor(BaseWorker):

        def run(self):
            while True:
                tag, *payload = self.recv()
                getattr(self, 'do_' + tag)(*payload)

        # Methods correponding to different message tags
        def do_A(self, x):
            print('Running A', x)

        def do_B(self, x, y):
            print('Running B', x, y)

    # Example
    a = TaggedActor()
    a.start()
    a.send(('A', 1))      # Invokes do_A(1)
    a.send(('B', 2, 3))   # Invokes do_B(2,3)
    a.close()
    a.join()

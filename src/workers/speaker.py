# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:38
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 16:34:51
import socket
from src.workers.base_worker import BaseWorker
from src.workers.base_worker import WorkerExit


class Speaker(BaseWorker):

    def __init__(self, frames):
        self.frames = frames
        self.speakSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super(Speaker, self).__init__()

    def __del__(self):
        try:
            self.speakSocket = None
        except AttributeError:
            pass

    def recv(self):
        msg = self._mailbox.get_nowait()
        if msg is WorkerExit:
            raise WorkerExit()
        return msg

    def run(self):
        host, port = self.recv()
        while True:
            host, port = self.recv()
            if len(self.frames) > 0:
                self.speakSocket.sendto(self.frames.pop(0), (host, port))

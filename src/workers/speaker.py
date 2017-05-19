# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:38
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 17:19:46
import socket
from src.workers.base_worker import Worker


class Speaker(Worker):

    def __init__(self, frames):
        self.frames = frames
        self.speakSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super(Speaker, self).__init__()

    def __del__(self):
        try:
            self.speakSocket = None
        except AttributeError:
            pass

    # def close(self):
    #     super(Speaker, self).close()
    #     self.speakSocket.close()

    def run(self):
        host, port = self.recv()
        while True:
            self.recv_nowait()
            if len(self.frames) > 0:
                self.speakSocket.sendto(self.frames.pop(0), (host, port))

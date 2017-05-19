# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 17:10:51
import socket
from src.workers.base_worker import Worker


class Listener(Worker):
    BUFFER = 1024
    CHANNELS = 2

    def __init__(self, frames, port=12000):
        self.frames = frames
        self.PORT = port
        super(Listener, self).__init__()

    def __del__(self):
        try:
            self.listenSocket.close()
        except AttributeError:
            pass

    def close(self):
        super(Listener, self).close()
        self.listenSocket.close()

    def run(self):
        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listenSocket.bind(('', self.PORT))
        while True:
            self.recv_nowait()
            soundData, addr = self.listenSocket.recvfrom(self.BUFFER * self.CHANNELS * 2)
            self.frames.append(soundData)

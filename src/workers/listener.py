# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 16:44:25
import socket
from src.workers.base_worker import BaseWorker


class Listener(BaseWorker):
    BUFFER = 1024
    CHANNELS = 2

    def __init__(self, frames, port=12000):
        self.frames = frames
        self.PORT = port
        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listenSocket.bind(('', self.PORT))
        super(Listener, self).__init__()

    def __del__(self):
        try:
            self.listenSocket.close()
        except AttributeError:
            pass

    def run(self):
        while True:
            soundData, addr = self.listenSocket.recvfrom(self.BUFFER * self.CHANNELS * 2)
            self.frames.append(soundData)

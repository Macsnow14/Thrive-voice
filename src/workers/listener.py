# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:34:07
import socket
from src.threads.base_worker import BaseWorker


class Listener(BaseWorker):
    BUFFER = 1024
    frames = None

    def __init__(self, queue, frames, port=12000):
        self.frames = frames
        self.PORT = port
        self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.voiceServerSocket.bind(('127.0.0.1', self.PORT))
        super(Listener, self).__init__(queue)

    def __del__(self):
        self.listenSocket.close()

    def run(self):
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_receive':
                    break
                else:
                    self.queue.put_nowait(data)
            soundData, addr = self.voiceServerSocket.recvfrom(self.BUFFER * self.CHANNELS * 2)
            self.frames.append(soundData)

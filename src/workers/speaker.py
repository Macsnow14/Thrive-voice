# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:38
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 15:43:57
import socket
from src.threads.base_worker import BaseWorker


class Speaker(BaseWorker):

    def __init__(self, frames, queue):
        self.frames = frames
        self.speakSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        super(Speaker, self).__init__(queue)

    def __del__(self):
        try:
            self.speakSocket = None
        except AttributeError:
            pass

    def run(self, host, dial_port):
        print('port is %s on host %s' % (dial_port, host))
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_send':
                    break
                else:
                    self.queue.put_nowait(data)
            if len(self.frames) > 0:
                self.listenSocket.sendto(self.frames.pop(0), (host, dial_port))

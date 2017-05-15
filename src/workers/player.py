# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:21:01
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:32:57
import pyaudio
from src.workers.base_worker import BaseWorker


class Player(BaseWorker):
    BUFFER = 1024
    FREAM_BUFFER = 10
    CHANNELS = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16
    frames = None

    def __init__(self, queue, frames):
        self.frames = frames
        self.p = pyaudio.PyAudio()
        super(Player, self).__init__(queue)

    def run(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             output=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_play':
                    break
                else:
                    self.queue.put_nowait(data)
            if len(self.frames) == self.FREAM_BUFFER:
                while True:
                    if len(self.frames) == 0:
                        break
                    stream.write(self.frames.pop(0), self.BUFFER)

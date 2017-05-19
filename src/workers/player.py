# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:21:01
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 17:02:57
import pyaudio
from src.workers.base_worker import Worker


class Player(Worker):
    BUFFER = 1024
    CHANNELS = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16

    def __init__(self, frames):
        self.frames = frames
        self.p = pyaudio.PyAudio()
        super(Player, self).__init__()

    def close(self):
        super(Player, self).close()
        self.p.close()

    def run(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             output=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            self.recv_nowait()
            if len(self.frames) != 0:
                stream.write(self.frames.pop(0), self.BUFFER)

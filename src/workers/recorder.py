# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:21:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-19 17:06:06
import pyaudio
from src.workers.base_worker import Worker


class Recorder(Worker):
    BUFFER = 1024
    CHANNELS = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16

    def __init__(self, frames):
        self.frames = frames
        self.p = pyaudio.PyAudio()
        super(Recorder, self).__init__()

    def close(self):
        super(Recorder, self).close()
        self.stream.close()

    def run(self):
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.BUFFER
                                  )
        while True:
            self.recv_nowait()
            self.frames.append(self.stream.read(self.BUFFER))

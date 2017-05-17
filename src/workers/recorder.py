# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:21:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-17 15:48:10
import pyaudio
from src.workers.base_worker import BaseWorker


class Recorder(BaseWorker):
    BUFFER = 1024
    CHANNELS = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16

    def __init__(self, frames):
        self.frames = frames
        self.p = pyaudio.PyAudio()
        super(Recorder, self).__init__()

    def run(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            self.frames.append(stream.read(self.BUFFER))

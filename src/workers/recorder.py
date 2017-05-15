# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:21:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:37:07
import pyaudio
from src.workers.base_worker import BaseWorker


class Recorder(BaseWorker):
    BUFFER = 1024
    CHANNELS = 2
    RATE = 44100
    FORMAT = pyaudio.paInt16
    frames = None

    def __init__(self, frames, queue):
        self.frames = frames
        self.p = pyaudio.PyAudio()
        super(Recorder, self).__init__(queue)

    def run(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.BUFFER
                             )
        while True:
            if not self.queue.empty():
                data = self.queue.get()
                if data == 'stop_record':
                    break
                else:
                    self.queue.put_nowait(data)
            self.outputFrames.append(stream.read(self.BUFFER))

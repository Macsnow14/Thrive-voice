# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:33
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:07:46
from src.threads.base_worker import BaseWorker


class Listener(BaseWorker):

    def __init__(self):
        super(Listener, self).__init__()

    def run(self):
        pass

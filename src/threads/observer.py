# -*- coding: utf-8 -*-
# @Author: Macsnow
# @Date:   2017-05-15 14:00:48
# @Last Modified by:   Macsnow
# @Last Modified time: 2017-05-15 14:07:04
from src.threads.base_worker import BaseWorker


class Observer(BaseWorker):

    def __init__(self):
        super(Observer, self).__init__()

    def run(self):
        pass

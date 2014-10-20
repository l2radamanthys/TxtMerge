#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import time



class MergeProcess(Thread):
    def __init__(self, files, output, gauge):
        Thread.__init__(self)
        self.is_run = True #bandera de proceso en ejecucion
        self.files = files
        self.output = output
        self.size = len(self.files)
        self.gauge = gauge



    def run(self):
        step = 0
        while step < self.size:
            path = self.files[step]
            #unir
            for line in open(path, 'r').readlines():
                self.output.write(line)
            self.gauge.step()
            #print step, line[:-1]
            step += 1
            time.sleep(0.05)
        self.is_run = False

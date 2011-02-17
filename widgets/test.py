#!/usr/bin/python

from tepwall.widget import Widget
import numpy

class Test(Widget):
    def load(self, panel):
        panel[:] = 0
        self.i = 0
    def update(self, panel):
        panel[numpy.unravel_index(self.i % len(panel.ravel()), panel.shape)] ^= -1
        self.i += 1

#!/usr/bin/python

from tepilepsy.widget import Widget

class Static(Widget):
    def __init__(self, image):
        self.image = image
    def update(self, panel):
        panel[:] = self.image

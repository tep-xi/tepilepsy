#!/usr/bin/python

from tepilepsy.widget import Widget
import cv, numpy

class Camera(Widget):
    def __init__(self, device=0, bright=True):
        self.device, self.bright = device, bright
    def load(self, panel):
        self.camera = cv.CaptureFromCAM(self.device)
    def update(self, panel):
        cv.Resize(cv.QueryFrame(self.camera), panel)
        cv.CvtColor(panel, panel, cv.CV_BGR2HSV)
        if self.bright: # increase saturation
            s = panel[..., 1]
            s += numpy.minimum(s, 255-s)
        cv.CvtColor(panel, panel, cv.CV_HSV2RGB)
    def unload(self):
        del self.camera

class BufferedCamera(Camera):
    def load(self, panel, bufsize):
        Camera.load(self, panel)
        self.buffer = numpy.repeat(panel[None], bufsize, 0)
        self.i = -1
    def update(self, panel):
        self.i = (self.i + 1) % len(self.buffer)
        Camera.update(self, self.buffer[self.i])
        self.generate(panel, self.buffer, self.i)
    def generate(self, panel, buffer, i):
        raise NotImplementedError

class DiffCamera(BufferedCamera):
    def load(self, panel):
        BufferedCamera.load(self, panel, 2)
    def generate(self, panel, buffer, i):
        #cv.Dilate(panel, panel, None, 1)
        cv.Smooth(panel, panel)
        panel[:] = numpy.subtract(*buffer)
        panel[:] = 1.3*(numpy.maximum(1.9*numpy.minimum(panel, -panel), 64) - 64)

class DelayCamera(BufferedCamera):
    def __init__(self, device=0, bright=True, delay=30):
        Camera.__init__(self, device, bright)
        self.delay = delay
    def load(self, panel):
        BufferedCamera.load(self, panel, self.delay)
    def generate(self, panel, buffer, i):
        panel[:] = buffer[(i+1) % self.delay]

class RelativisticCamera(BufferedCamera):
    def load(self, panel):
        BufferedCamera.load(self, panel, panel.shape[1])
    def generate(self, panel, buffer, i):        
        for col in range(len(buffer)):
            panel[:,col] = buffer[(col+i+1) % len(buffer),:,col]

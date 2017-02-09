from tepilepsy.widget import Widget
from time import time
from multiprocessing import Process
from tempfile import mkstemp
from subprocess import check_call
import numpy as np
import moviepy.editor as mov
import os

class Video(Widget):
    def __init__(self, filename):
        self._filename = filename
    def load(self, panel):
        if os.path.isfile(self._filename):
            self._video = mov.VideoFileClip(self._filename)
        else:
            (hdl, tempfile) = mkstemp()
            check_call(['youtube-dl', '-q', '--no-playlist', '-o', '-', self._filename], stdout=hdl)
            os.close(hdl)
            self._video = mov.VideoFileClip(tempfile)
        self._video = self._video.resize(newsize=(panel.shape[1],panel.shape[0]))
        self._t0 = time()
        #Process(target=self._video.audio.preview).start()
    def update(self, panel):
        t1 = time()
        dt = t1 - self._t0
        if dt > self._video.duration:
            self._t0 = t1
        panel[:] = self._video.get_frame(dt)

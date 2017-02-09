from tepilepsy.widget import *
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import numpy

class Plot(Tepilepsy):
    def __init__(self):
        self.im = None
    def start(self, widget, fps=30):
        self.widget = widget
        fig = plt.figure()
        self.arr = numpy.zeros((36,60,3), dtype='ubyte')
        self.widget.load(self.arr)
        self.widget.update(self.arr)
        self.im = plt.imshow(self.arr, animated=True)
        anim = ani.FuncAnimation(fig, self.update, interval=1000./fps)
        plt.show()
    def update(self, *args):
        try:
            self.widget.update(self.arr)
        except Exception as e:
            print(e)
        self.im.set_array(self.arr)
        return self.im

from multiprocessing import Process, Event, Pipe
import numpy, tepwall.dmx

# Important note: Python multiprocessing is VERY STRANGE.  Once a
# widget is started, its state is not communicated back to the main
# thread.

"""
To use the widget architecture:

1. Make a class that's a subclass of 'widget.Widget'
2. Call 'widget.start' on your custom widget
3. To run a different widget, just call 'widget.start' again
4. Call 'widget.stop' to halt rendering
"""

class Widget(object):
    def __init__(self, *args, **kwargs):
        pass
    def load(self, shape):
        pass
    def update(self, panel):
        raise NotImplementedError
    def unload(self):
        pass

class Tepilepsy(object):
    def __init__(self):
        pass
    def start(self, widget, fps=30):
        pass
    def stop(self):
        pass

class Tepwall(Tepilepsy):
    def __init__(self):
        (self._recv, self._send), self._go = Pipe(False), Event()
        self._proc = Process(target=self._execute, args=(self._recv, self._go))
        self._proc.daemon = True
        self._proc.start()
    def _execute(self, widget_pipe, go):
        panel = numpy.zeros((36,60,3), dtype='ubyte')
        while go.wait():
            try:
                widget, fps = widget_pipe.recv()
                widget.load(panel)
                widget.update(panel)
                while go.is_set() and not widget_pipe.poll(1./fps):
                    widget.update(panel)
                    tepwall.dmx.display(panel)
                widget.unload()
            except Exception as e:
                print(e)
                go.clear()
    def start(self, widget, fps=30):
        self._send.send((widget, fps))
        self._go.set()
    def stop(self):
        self._go.clear()

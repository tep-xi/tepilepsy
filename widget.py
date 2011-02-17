from multiprocessing import Process, Event, Pipe

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

class Widget:
    def __init__(self, *args, **kwargs):
        pass
    def load(self, shape):
        pass
    def update(self, panel):
        raise NotImplementedError
    def unload(self):
        pass

def _execute(widget_pipe, go):
    import dmx, numpy
    panel = numpy.zeros((36,60,3), dtype='ubyte')
    while go.wait():
        try:
            widget, fps = widget_pipe.recv()
            widget.load(panel)
            widget.update(panel)
            while go.is_set() and not widget_pipe.poll(1./fps):
                widget.update(panel)
                dmx.display(panel)
            widget.unload()
        except Exception as e:
            print(e)
            go.clear()

(_recv, _send), _go = Pipe(False), Event()
_proc = Process(target=_execute, args=(_recv, _go))
_proc.daemon = True
_proc.start()

def start(widget, fps=30):
    _send.send((widget, fps))
    _go.set()
def stop():
    _go.clear()

from tepwall.widget import Widget
import numpy

class Compose(Widget):
    def __init__(self, func=None, *widgets):
        self.widgets = widgets
        if func: self.func = func
    def load(self, panel):
        for w in self.widgets: w.load(panel)
    def update(self, panel):
        if not hasattr(self, 'buffer'):
            self.buffer = numpy.empty_like(panel)
        self.widgets[0].update(panel)
        for w in self.widgets[1:]:
            w.update(self.buffer)
            self.func(panel, self.buffer)
    def unload(self):
        for w in self.widgets: w.unload()

from tepilepsy.widget import Widget
from tepilepsy import text

class Marquee(Widget):
    def __init__(self, font, string, rate=1, color=[255,255,255]):
        self.message = text.get_row(font, string)
        self.rate, self.color, self.i = rate, color, 0
    def load(self, panel):
        self.pw, self.mw = panel.shape[1], self.message.shape[1]
        vmin = (panel.shape[0] - self.message.shape[0]) // 2
        self.vrange = slice(vmin, vmin+self.message.shape[0])
    def update(self, panel):
        panel[:] = 0
        p1, p2 = max(self.pw - self.i, 0), min(self.pw + self.mw - self.i, self.pw)
        m1, m2 = max(self.i - self.pw, 0), min(self.i, self.mw)
        panel[self.vrange,p1:p2] = self.color * self.message[:,m1:m2,None]
        self.i = (self.i + 1./self.rate) % (self.pw + self.mw)

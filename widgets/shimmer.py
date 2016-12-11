import cv2, time
from tepwall.widget import Widget
from numpy import sin, cos, square, linspace

class Shimmer(Widget):
    def __init__(self, a=1.5, b=22, c=60, d=.522222, e=.71, saturation=255, brightness=255):
        """
        a ~ speed of shape change
        b ~ speed of hue change
        c ~ density of contours
        d ~ x velocity of center
        e ~ y velocity of center
        """
        self.consts = a, b, c, d, e, saturation, brightness
    def load(self, panel):
        self.i = (linspace(-1, 1, panel.shape[1]),
                  linspace(-1, 1, panel.shape[0])[:,None])
    def update(self, panel):
        (a, b, c, d, e, saturation, brightness), (x, y), t = self.consts, self.i, time.time()
        panel[...,0] = (c*cos(a*t)*square(x-cos(d*t))+b*t+
                        c*sin(a*t)*square(y-sin(e*t)))%180
        panel[...,1] = saturation
        panel[...,2:] = brightness
        cv2.cvtColor(panel, cv2.COLOR_HSV2RGB, panel)


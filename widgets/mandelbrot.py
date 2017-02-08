import cv2, time, numpy
from tepwall.widget import Widget
from numpy import linspace

def dist2(x, y):
    (x0, x1), (y0, y1) = x, y
    return (y0 - x0)*(y0 - x0) + (y1 - x1)*(y1 - x1)

def mandelbrot(c, max_iters):
    z = c
    for i in range(max_iters):
        r = abs(z)
        if r > 2:
            return 1 + i - numpy.log2(numpy.log(r))
        z = z*z + c
    return max_iters

class Mandelbrot(Widget):
    def __init__(self, max_iters, scale, bounds=((-2, 2), (-2, 2)), dtype=numpy.longdouble):
        self.max_iters = max_iters
        self.scale = scale
        self.bounds = bounds
        self.dtype = dtype
    def load(self, panel):
        self.vals = self.bounds, time.time(), True
    def update(self, panel):
        ((xb, yb), oldtime, newzoom) = self.vals
        xs = linspace(xb[0], xb[1], panel.shape[1], dtype=self.dtype)
        ys = linspace(yb[0], yb[1], panel.shape[0], dtype=self.dtype)
        mset = (set(), set())
        localmaxiters = 1
        for i in range(panel.shape[0]):
            for j in range(panel.shape[1]):
                iters = mandelbrot(xs[j] + 1j * ys[i], self.max_iters)
                panel[i, j, 0] = iters
                if iters > localmaxiters:
                    localmaxiters = iters
        for i in range(panel.shape[0]):
            for j in range(panel.shape[1]):
                iters = panel[i, j, 0]
                if iters == self.max_iters:
                    mset[0].add((i, j))
                    mset[1].update([(i+1, j), (i, j+1), (i-1, j), (i, j-1)])
                    panel[i, j, :] = (0, 0, 0)
                else:
                    if iters > localmaxiters * 19 / 20:
                        mset[1].update([(i+1, j), (i, j+1), (i-1, j), (i, j-1)])
                    panel[i, j, :] = (180 * iters / localmaxiters, 192 + 63 * iters / localmaxiters, 255)
        cv2.cvtColor(panel, cv2.COLOR_HSV2RGB, panel)
        boundary = mset[1] - mset[0]
        newtime = time.time()
        tdiff = newtime - oldtime
        npixels = panel.shape[0] * panel.shape[1]
        xr = (xb[1] - xb[0]) / 2 * self.scale
        yr = (yb[1] - yb[0]) / 2 * self.scale
        if 100 * len(mset[0]) < npixels or len(boundary) == 0 or 2 * len(mset[0]) > npixels or min(xr, yr) < numpy.finfo(self.dtype).resolution * 10:
            self.vals = self.bounds, newtime, True
        else:
            zoomn = boundary.pop()
            if not newzoom:
                center = (panel.shape[0]/2, panel.shape[1]/2)
                for point in boundary:
                    if dist2(point, center) < dist2(zoomn, center):
                        zoomn = point
            xz, yz = xs[zoomn[1]], ys[zoomn[0]]
            self.vals = ((xz - xr, xz + xr), (yz - yr, yz + yr)), newtime, False

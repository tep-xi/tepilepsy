import cv2, time, numpy, math
from tepwall.widget import Widget
from numpy import linspace
from numba import jit

@jit(cache=True, nopython=True, nogil=True)
def dist2(x, y):
    (x0, x1), (y0, y1) = x, y
    return (y0 - x0)*(y0 - x0) + (y1 - x1)*(y1 - x1)

@jit(cache=True, nopython=True, nogil=True)
def mandelbrot(c, max_iters):
    z = c
    for i in range(max_iters):
        r = abs(z)
        if r > 2:
            return 1 + i - numpy.log2(numpy.log(r))
        z = z*z + c
    return max_iters

@jit(cache=True, nopython=True, nogil=True)
def numiters(xr, yr):
    return int(223.0 / numpy.sqrt(0.001 + 2.0 * min(xr, yr)))

class Mandelbrot(Widget):
    def __init__(self, scale=0.99, bounds=((-2.0, 2.0), (-1.2, 1.2)), dtype=numpy.float64):
        self.scale = scale
        self.ogbounds = bounds
        self.bounds = bounds
        self.dtype = dtype
        self.oldzoom = None
        self.max_iters = numiters(bounds[0][1] - bounds[0][0], bounds[1][1] - bounds[1][0])
    def load(self, panel):
        pass #self.iterray = numpy.empty((panel.shape[0], panel.shape[1]), dtype=numpy.int64)
    @jit(cache=True)
    def update(self, panel):
        (xb, yb), oldzoom = self.bounds, self.oldzoom
        xs = linspace(xb[0], xb[1], panel.shape[1], dtype=self.dtype)
        ys = linspace(yb[0], yb[1], panel.shape[0], dtype=self.dtype)
        mset = (set([-1]), set([-1]))
        for i in range(panel.shape[0]):
            for j in range(panel.shape[1]):
                iters = mandelbrot(xs[j] + 1j * ys[i], self.max_iters)
                if iters == self.max_iters:
                    mset[0].add((i, j))
                    mset[1].update([(i+1, j), (i, j+1), (i-1, j), (i, j-1)])
                    panel[i, j, :] = (0, 0, 0)
                else:
                    #if iters > localmaxiters * 19 / 20:
                    #    mset[1].update([(i+1, j), (i, j+1), (i-1, j), (i, j-1)])
                    panel[i, j, :] = (180 * iters / self.max_iters, 192 + 63 * iters / self.max_iters, 255)
        cv2.cvtColor(panel, cv2.COLOR_HSV2RGB, panel)
        boundary = mset[1] - mset[0]
        npixels = panel.shape[0] * panel.shape[1]
        xr = xb[1] - xb[0]
        yr = yb[1] - yb[0]
        xr2 = xr / 2 * self.scale
        yr2 = yr / 2 * self.scale
        if 100 * len(mset[0]) < npixels or len(boundary) == 0 or min(xr, yr) < numpy.finfo(self.dtype).resolution * 10:
            self.bounds = self.ogbounds
            self.oldzoom = None
            bounds = self.bounds
            self.max_iters = numiters(bounds[0][1] - bounds[0][0], bounds[1][1] - bounds[1][0])
        else:
            zoomn = boundary.pop()
            if oldzoom is not None:
                oldzoomd = (xs[oldzoom[1]-1], ys[oldzoom[0]-1])
                for point in boundary:
                    pointd = (xs[point[1]-1], ys[point[0]-1])
                    if dist2(point, oldzoom) < dist2(zoomn, oldzoom):
                        zoomn = point
            xz, yz = xs[zoomn[1]], ys[zoomn[0]]
            self.bounds = ((xz - xr2, xz + xr2), (yz - yr2, yz + yr2))
            self.oldzoom = zoomn
            self.max_iters = numiters(xr, yr)

import cv2, time, numpy, math, random
from tepilepsy.widget import Widget
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

@jit(cache=True, nopython=True, nogil=True)
def p2v(p, xs, ys):
    return (xs[p[1]-1], ys[p[0]-1])

@jit(cache=True, nopython=True, nogil=True)
def updateloop(panel, samples, max_iters, xs, xstep, ys, ystep, hueoffset):
    for i in range(panel.shape[0]):
        for j in range(panel.shape[1]):
            panel[i, j, :] = (0, 0, 0)
            for sample in range(samples):
                prex, prey = numpy.random.random(2)
                pt = (xstep * prex + xs[j], ystep * prey + ys[i])
                iters = mandelbrot(pt[0] + 1j * pt[1], max_iters)
                if iters != max_iters:
                    panel[i, j, 0] += int((180 * iters / max_iters) / samples + hueoffset) % 256
                    panel[i, j, 1] += int((192 + 63 * iters / max_iters) / samples)
                    panel[i, j, 2] += int(255 / samples)

@jit(cache=True, nopython=True, nogil=True)
def getmset(samples, panel):
    mset = (set([(-1, -1)]), set([(-1, -1)]))
    maxval = samples * int(255 / samples)
    for i in range(panel.shape[0]):
        for j in range(panel.shape[1]):
            if panel[i, j, 2] != maxval:
                mset[0].add((i, j))
                mset[1].update([(i+1, j), (i, j+1), (i-1, j), (i, j-1)])
    return mset

@jit(cache=True, nopython=True, nogil=True)
def dozoom(boundary, oldzoom, zoomnd, xs, ys):
    for point in boundary:
        pointd = p2v(point, xs, ys)
        if dist2(pointd, oldzoom) < dist2(zoomnd, oldzoom):
            zoomn = point
            zoomnd = pointd
    return zoomnd

class Mandelbrot(Widget):
    def __init__(self, scale=0.975, bounds=((-2.0, 2.0), (-1.2, 1.2)), dtype=numpy.float64, samples=4):
        self.scale = scale
        self.ogbounds = bounds
        self.bounds = bounds
        self.dtype = dtype
        self.samples = samples
        self.oldzoom = None
        self.max_iters = numiters(bounds[0][1] - bounds[0][0], bounds[1][1] - bounds[1][0])
        self.hueoffset = random.randint(0,255)
    def load(self, panel):
        pass
    @jit(cache=True)
    def update(self, panel):
        t0 = time.time()
        (xb, yb), oldzoom = self.bounds, self.oldzoom
        xs, xstep = linspace(xb[0], xb[1], panel.shape[1], dtype=self.dtype, retstep=True)
        ys, ystep = linspace(yb[0], yb[1], panel.shape[0], dtype=self.dtype, retstep=True)
        updateloop(panel, self.samples, self.max_iters, xs, xstep, ys, ystep, self.hueoffset)
        mset = getmset(self.samples, panel)
        cv2.cvtColor(panel, cv2.COLOR_HSV2RGB, panel)
        boundary = mset[1] - mset[0]
        npixels = panel.shape[0] * panel.shape[1]
        xr = xb[1] - xb[0]
        yr = yb[1] - yb[0]
        if 100 * len(mset[0]) < npixels or len(boundary) == 0 or min(xr, yr) < numpy.finfo(self.dtype).resolution * 10 or time.time() - t0 > 1.2:
            self.bounds = self.ogbounds
            self.oldzoom = None
            bounds = self.bounds
            self.max_iters = numiters(bounds[0][1] - bounds[0][0], bounds[1][1] - bounds[1][0])
            self.hueoffset = random.randint(0,255)
        else:
            zoomn = boundary.pop()
            zoomnd = p2v(zoomn, xs, ys)
            if oldzoom is not None:
                newzoom = dozoom(boundary, oldzoom, zoomnd, xs, ys)
                zoomnd = 0.3 * numpy.array(newzoom) + 0.7 * numpy.array(oldzoom)
            (xz, yz) = zoomnd
            xr2 = xr / 2 * self.scale
            yr2 = yr / 2 * self.scale
            self.bounds = ((xz - xr2, xz + xr2), (yz - yr2, yz + yr2))
            self.oldzoom = zoomnd
            self.max_iters = numiters(xr, yr)
            self.hueoffset += random.random()/4

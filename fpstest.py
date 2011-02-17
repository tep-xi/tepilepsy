#!/usr/bin/python

import time, numpy, dmx

output = numpy.zeros((36,60,3),'ubyte')
while True:
    t = time.time()
    for i in range(1000):
        output[numpy.random.randint(36),numpy.random.randint(60)]=numpy.random.rand(3)*255
        dmx.display(output)
    print('{0} fps'.format(1000./(time.time()-t)))
    

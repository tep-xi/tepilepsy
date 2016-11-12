from numpy import zeros, asarray, rollaxis
import socket

# Create socket connections to the two controllers
def connect(ip_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    sock.connect((ip_address, 6038))
    return sock
dmx = [connect(socket.gethostbyname(host)) for host in ['tepilepsy.mit.edu', 'lepitepsy.mit.edu']]

# Allocate a buffer for transmitted packets and fill it with magic
xmit = zeros(681, dtype='ubyte')
xmit[:8],xmit[17],xmit[21],xmit[-1] = [4,1,220,74,1,0,8,1],209,2,191

# Display the array-like object "panel" that has shape (36,60,3).
def display(panel):
    for i in range(30):
        xmit[16], x, y, k = 1+(i%16), 12*(i//10), 6*(i%10), 2*(i%2)-1
        xmit[24:240] = rollaxis(asarray(panel)[x:x+12,y:y+6][::-1,::k],1).ravel()
        dmx[i//16].sendall(xmit)

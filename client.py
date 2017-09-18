import sys
import socket
from struct import *
from PIL import Image
from multiprocessing import Pool

# python3 client.py localhost 1234 1.png 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], int(sys.argv[2])))
sock.send(pack("!B", 0) )

def pixel(x,y,r,g,b,a=255):
  if a == 255:
    sock.send( 
        (x).to_bytes(2, byteorder='big')
      + (y).to_bytes(2, byteorder='big')
      + pack("!3B", r, g, b) 
        )

def qpixel(position):
  position = map(int, position)
  x1, x2, y1, y2 = position
  im = Image.open(sys.argv[3]).convert('RGBA')
  print (im)
  for x in range(x1, x2):
    for y in range(y1, y2):
        r, g, b, a = im.getpixel((x, y))
        sock.send( 
        (x).to_bytes(2, byteorder='big')
      + (y).to_bytes(2, byteorder='big')
      + pack("!3B", r, g, b) 
        )

im = Image.open(sys.argv[3]).convert('RGBA')
_,_,w,h = im.getbbox()
p = Pool(16)
p.map(qpixel, [
    (0, w/4, 0, h/4),
    (w/4, w/4*2, 0, h/4),
    (w/4*2, w/4*3, 0, h/4),
    (w/4*3, w/4*4, 0, h/4),
    (0, w/4*2, h/4, h/4*2),
    (0, w/4*2, h/4*2, h/4*3),
    (0, w/4*2, h/4*3, h/4*4),
    (w/4, w/4*2, h/4, h/4*2),
    (w/4, w/4*2, h/4*2, h/4*3),
    (w/4, w/4*2, h/4*3, h/4*4),
    (w/4*2, w/4*3, h/4, h/4*2),
    (w/4*2, w/4*3, h/4*2, h/4*3),
    (w/4*2, w/4*3, h/4*3, h/4*4),
    (w/4*3, w/4*4, h/4, h/4*2),
    (w/4*3, w/4*4, h/4*2, h/4*3),
    (w/4*3, w/4*4, h/4*3, h/4*4),
    ]
    )

import sys
import socket
from struct import *
from PIL import Image


# python3 client.py localhost 1234 1.png 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], int(sys.argv[2])))

def pixel(x,y,r,g,b,a=255):
  if a == 255:
    sock.send( 
        (x).to_bytes(2, byteorder='big')
      + (y).to_bytes(2, byteorder='big')
      + pack("!3B", r, g, b) 
        )

im = Image.open(sys.argv[3]).convert('RGBA')
_,_,w,h = im.getbbox()
sock.send(pack("!B", 0) )
for x in range(w):
  for y in range(h):
    r,g,b,a = im.getpixel((x,y))
    pixel(x,y,r,g,b,a)

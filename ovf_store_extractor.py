#!/bin/env python
import sys

file = "ovf_store"
markoffset = 257

f = open (file, 'r')
total = 0
last_total = 0
try:
  buf = open ("empty" , 'a')
  while True:
    read_buffer = f.read(512)
    if not read_buffer:
      break
    total += 512
    index = read_buffer.find("ustar")
    if index != -1:
      if index < markoffset:
        print "Failed :( %d " %read_buffer.index("ustar")
        sys.exit(1)
      else:
        if index > markoffset:
          buf.write (read_buffer[:index - markoffset - 1])
        buf.close()
        buf = open ("ovf_%d" %(total - 512 - markoffset + index), 'a')
        buf.write(read_buffer[index - markoffset:])
    else:
      buf.write(read_buffer)
except Exception:
  print total
  f.close()
  raise
f.close()

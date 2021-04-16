import glob
import os

paths = glob.glob('/usr/local/etc/haproxy/conf.d/*.cfg')
file ='/usr/local/etc/haproxy/haproxy.cfg'

with open(file, 'a+') as outfile:
 for path in paths:
  with open(path) as infile:
   outfile.write("\n")
   outfile.write(infile.read())
 if os.path.exists(path):
  os.remove(path)

f = open(file, "a+")
f.write("\n")
f.close()
 
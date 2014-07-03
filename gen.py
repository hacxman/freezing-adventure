import random
from operator import add
import sys

lb = [reduce(add, [chr(random.randrange(ord('a'), ord('z'))) for l in range(random.randrange(5,7))], '') for n in xrange(2 + int(sys.argv[1])/200)]

def geni():
    rc = random.random()
    r = random.random()
    r0 = random.randrange(0, 8)
    if rc < 0.3:
      sys.stdout.write("c")
    if r < 0.1:
      print "nop"
    elif r >= 0.1 and r < 0.2:
      l = lb[random.randrange(0, len(lb))]
      print "ld %%%i" % r0, l
    elif r >= 0.2 and r < 0.266:
      l = lb[random.randrange(0, len(lb))]
      print "st %%%i" % r0, l
    elif r >= 0.266 and r < 0.33:
      r1 = random.randrange(0, 8)
      r2 = random.randrange(0, 8)
      #l = lb[random.randrange(0, len(lb))]
      print "ld %{} %{} %{}".format(r0,r1,r2)
    elif r >= 0.33 and r < 0.4:
      r1 = random.randrange(0, 8)
      r2 = random.randrange(0, 8)
      #l = lb[random.randrange(0, len(lb))]
      print "st %{} %{} %{}".format(r0,r1,r2)
      #print "st %%%i" % r0, l
    elif r >= 0.4 and r < 0.6:
      r1 = random.randrange(0, 8)
      print "mov %%%i %%%i" % (r0, r1)
    elif r >= 0.6 and r < 0.8:
      rval = random.randrange(0, 256)
      print "mov %%%i" % (r0), rval
    elif r >= 0.8 and r < 0.9:
      r1, r2 = random.randrange(0, 8), random.randrange(0, 8)
      print 'add %%%i %%%i %%%i' % (r0, r1, r2)
    elif r >= 0.9 and r < 1:
      r1, r2 = random.randrange(0, 8), random.randrange(0, 8)
      print 'sub %%%i %%%i %%%i' % (r0, r1, r2)

def genl():
    l =  lb[random.randrange(0, len(lb))]
    print "%s:" % l

[geni() if random.random() > 0.2 else genl() for x in xrange(int(sys.argv[1]))]


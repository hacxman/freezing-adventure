import os
import sys
import re

def failwith(m):
  sys.stderr.writelines(m)
  exit(1)

class Label(object):
  def __init__(self, name):
    global curln
    self.name = name
    self.addr = None
    self.line = curln
  def show(self):
    print "Label [@%s]"%str(self.addr), self.name
  def machine_length(self):
    return 0
  def get_machine_code(self):
    return []

class Name(object):
  def __init__(self, idx):
    self.name = str(idx)
  def __repr__(self):
    return "%s"%(self.name)

class Reg(object):
  def __init__(self, idx):
    self.name = int(idx)
  def __repr__(self):
    return "r%i"%(self.name)

class Addr(object):
  def __init__(self, idx):
    self.name = int(idx)
  def __repr__(self):
    return "%i"%(self.name)

class Num(object):
  def __init__(self, idx):
    self.name = int(idx)
  def __repr__(self):
    return "%i"%(self.name)

class Instr(object):
  def __init__(self, name, args):
    global curln
    self.name = name
    self.args = map(self.parse_arg, args)
    self.addr = None
    self.line = curln
  def show(self):
    print "Instr [@%s]"%str(self.addr), self.name, self.args
  def machine_length(self):
    return 1

  def try_num(self, arg):
    if arg.isdigit():
      return Num(int(arg))
    else:
      return  None
  def try_addr(self, arg):
    global curln
    if arg[0] == '[' and arg[-1] == ']':
      if arg[1:-1].isdigit():
        return Addr(arg[1:-1])
      else:
        failwith("invalid address '%s' at line %i\n" %(arg, curln))
    else:
      return None
  def try_reg(self, arg):
    global curln
    if arg[0] == '%':
      if arg[1:].isdigit():
        return Reg(arg[1:])
      else:
        failwith("invalid register name '%s' at line %i\n" %(arg, curln))
    else:
      return None
  def try_name(self, arg):
    if arg[0].isalpha() and arg[1:].isalnum():
      return Name(arg)
    else:
      return None

  def parse_arg(self, arg):
    global curln
    r = dropnone([self.try_num(arg), self.try_addr(arg), self.try_reg(arg), self.try_name(arg)])
    if not r == []:
#      print "arg",arg, "parsed succesfully!1!"
      return r[0]
    else:
      failwith("unrecognized argument type of '%s' at line %i\n" %(arg, curln))

  def get_machine_code(self):
    global curln, totallns
    curln += 1
    sys.stdout.write("%i/%i   \r" % (curln, totallns))
    if self.name == 'nop':
      if len(self.args) > 0:
        failwith("nop should have 0 args, has %s at line %i\n" % (self.args, self.line))
      return [0]
    elif self.name == 'mov':
      if len(self.args) != 2:
        failwith("mov has arity 2, not %i at line %i\n" %(len(self.args), self.line))
      if self.args[0].__class__.__name__ == Reg.__name__:
        if self.args[1].__class__.__name__ == Reg.__name__:
          return [(self.args[0].name << 4) + 0b0010, (self.args[1].name & 0b111) << 4]
        elif self.args[1].__class__.__name__ == Num.__name__:
          return [(self.args[0].name << 4) + 0b0010, self.args[1].name]
        else:
          failwith("2st argument of mov should be register or number, not %s at line %i\n" %(self.args[1], self.line))
      else:
        failwith("1st argument of mov should be register, not %s at line %i\n" %(self.args[0], self.line))
    elif self.name in ['ld', 'st']:
      if len(self.args) != 2:
        failwith("ld has arity 2, not %i at line %i\n" %(len(self.args), self.line))
      if self.args[0].__class__.__name__ == Reg.__name__:
        if self.args[1].__class__.__name__ == Addr.__name__:
          opcode = 0b0010 if self.name == 'ld' else 0b0100
          return [((self.args[0].name & 0b111) << 4) + opcode, self.args[1].name & 0xff]
        else:
          failwith("2st argument of ld/st should be address, not %s at line %i\n" %(self.args[1], self.line))
      else:
        failwith("1st argument of mov should be register, not %s at line %i\n" %(self.args[0], self.line))
    elif self.name in ['add', 'sub']:
      if len(self.args) != 3:
        failwith("ld has arity 3, not %i at line %i\n" %(len(self.args), self.line))
      if self.args[0].__class__.__name__ == Reg.__name__:
        if self.args[1].__class__.__name__ == Reg.__name__:
          if self.args[2].__class__.__name__ == Reg.__name__:
            opcode = {'add':0b1001, 'sub':0b1010}[self.name]
            return [((self.args[0].name & 0b111) << 4) + opcode, ((self.args[1].name & 0b111) << 4) + (self.args[2].name & 0b111)]
          else:
            failwith("3st argument of mov should be register, not %s at line %i\n" %(self.args[2], self.line))
        else:
          failwith("2st argument of mov should be register, not %s at line %i\n" %(self.args[1], self.line))
      else:
        failwith("1st argument of mov should be register, not %s at line %i\n" %(self.args[0], self.line))
    else:
      failwith("unsupported instruction %s at line %i\n" % (self.name, self.line))


curln = 0
totallns = 0

def parseline(line):
  global curln, totallns
  curln += 1
  sys.stdout.write("%i/%i   \r" % (curln, totallns))
  p = re.match("^(\w+):(.*)$", line)
  if p is not None:
    if len(p.groups()[1]) > 0:
      failwith('garbadge in label at line %i\n' % curln);
    if len(p.groups()[0]) < 1:
      failwith('label name at line %i must be at least 1 chr long\n' % curln);
    return Label(p.groups()[0])
  else:

#    p = re.match("^\s*(\w+)\s([%a-zA-Z0-9 ]*)$", line)
    p = line.split()
    if p == []:
      return None
    r = re.match("^\w+$", p[0])
    if r is not None:
      return Instr(p[0], p[1:])
#      if p.groups()
    else:
      failwith('malformed instruction name at line %i\n' % curln)

    # now try if it is instruction
    pass
  return None

def dropnone(lst):
  return filter(lambda x: x is not None, lst)

#  r = []
#  for i in lst:
#    if i is not None:
#      r.append(i)
#  return r

def compute_addresses(ast, offset = None):
  print "compute addresses"
  addr = 0
  if offset is not None:
    addr = offset

  r = []
  ln = len(ast)
  for _i, i in enumerate(ast):
    sys.stdout.write("%i/%i   \r" % (_i, ln))
#    print i.__class__.__name__
    if i.__class__.__name__ in [Label.__name__, Instr.__name__]:
      i.addr = addr
      addr += i.machine_length()
    else:
      failwith("can't compute address, unsupported mnemonic '%s'\ncurrent address is %i, line %i\n" % (str(i), addr, i.line))


def resolve_referencies(ast):
  print "resolve referencies"
  labels = {str(l.name):l.addr
      for l in filter(lambda x: x.__class__.__name__ == Label.__name__, ast)}

#  print labels['rofl']

  # walk ast for names
  ln = len(ast)
  for _i, i in enumerate(ast):
    sys.stdout.write("%i/%i   \r" % (_i, ln))
#    print i
    if i.__class__.__name__ == Instr.__name__:
#      print 'yes,'
      nargs = []
      for a in i.args:
#        print a
        if a.__class__.__name__ == Name.__name__:
          if labels.has_key(a.name):
            nargs.append(Addr(labels[a.name]))
          else:
            failwith("unknown label name '%s' at line %i\n" % (a, i.line))
        else:
          nargs.append(a)
      i.args = nargs

def _print(x):
  print x

from operator import add, concat

def parse(lines):
  global totallns, curln
  totallns = len(lines)
  ls = dropnone(map(parseline, lines))
#  map(lambda x: x.show(), ls)
#  print ls
  compute_addresses(ls)
#  map(lambda x: x.show(), ls)
  resolve_referencies(ls)
#  map(lambda x: x.show(), ls)
  curln = 0
  totallns = len(ls)
  print 'get machine code'
  mc = map(lambda x: x.get_machine_code(), ls)

  return mc


if __name__=="__main__":
  fname = sys.argv[1]
  with open(fname) as fin:
    mc = parse(fin.readlines())

  #map(lambda x: _print(bin(x)), mc)

  print 'write file'
  with open(sys.argv[1]+".out", "wb+") as fout:
    map(lambda x: fout.write(bytearray(x)), mc)

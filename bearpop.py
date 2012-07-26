#!/usr/bin/python2

import numpy as np
import time
from subprocess import call
from math import log

timeFile = "timeintervals.data"
picfolder = "outfiles"
picbase = "pic"
remake = ".remake"

n = 51 # rows
m = 51 # columns
v = 0.02 # bear velocity (cycles/bears)
r = v/10 # probability of random walk in a direction
N = 500000 # number of time cycles
Bn = n*m/10 # number of bears

timemult = 100
redraw = 15 # frequency of redraw

# potential matrix, high values are undesirable (unstable)
# measured in dead bear units
# this is initialized in main() using getPotential()
PP = None

# fundamental function of model, compute probability of move to new square
def Pmove(ifrom, ito, Bmap):
  # use a potential model of movement
  def P(i):
    return Bmap[i] + PP[i]
  return v * (P(ifrom) - P(ito)) * H(P(ifrom) - P(ito)) + r

# return list of tuples of initial bear locations
def initialize():
  #return [(np.random.random_integers(n)-1, np.random.random_integers(m)-1) for num in range(Bn)]
  return [(n // 2,m // 2) for num in range(Bn)]


call(["mkdir", "-p", picfolder])
timeIntervalF = open(timeFile, 'w')
call(["touch", remake])
def process(bears, k, Rk):
  tk = int(round(timeInterval(Rk)*timemult))
  tk = tk if tk>0 else 1
  timeIntervalF.write(str(k) + ' ' + str(tk) + '\n')
  prettyprint(bears)
  print
  print
  time.sleep(0.1)
  call(["scrot", "-e", "mv $f " + picfolder + "/" + picbase + str(k) + ".png"])


def getPotential():
  PP = np.zeros([n,m])
  # this example will cause a net migration to the right with some arbitrary potential wells
  for i in range(m):
    PP[:,i] = -i/15.

  #addLinearWell(PP, (n // 2,     m // 3    ), m / 2, .3 ) 
  #addLinearWell(PP, (3 * n // 4, 2 * m // 3), m / 4, .5  ) 
  #addLinearWell(PP, (n // 4,     2 * m // 3), m / 4, .5  ) 

  #addLinearWellLine(PP, (n // 2,     0), (n // 2,     m), m / 4, 1  ) 
  #addLinearWellLine(PP, (0,     m // 2), (n,     m // 2), n / 4, 1  ) 
  #addLinearWell(PP, (n // 2,     m // 2), m / 4, -1  ) 
  # not exactly a cross but close

  addLinearWellLine(PP, (0,     3 * m//4), (n,     3*m//4 ), 2, -1  ) 
  addLinearWell(PP, (n//2, 3 * m//4), 2, 1)

  return PP

def main():
  # get initial bear locations
  bears = initialize()

  # initialize bear map
  Bmap = getBmap(bears)

  # initialize potential well
  global PP
  PP = getPotential()

  for k in range(N):
    Rk = 0
    for bi in range(len(bears)):
      Pu = Pd = Pl = Pr = 0
      if bears[bi][0]>0:
        Pu = Pmove(bears[bi], (bears[bi][0] - 1, bears[bi][1]), Bmap)
      if bears[bi][0]<n-1:
        Pd = Pmove(bears[bi], (bears[bi][0] + 1, bears[bi][1]), Bmap)
      if bears[bi][1]>0:
        Pl = Pmove(bears[bi], (bears[bi][0], bears[bi][1] - 1), Bmap)
      if bears[bi][1]<m-1:
        Pr = Pmove(bears[bi], (bears[bi][0], bears[bi][1] + 1), Bmap)

      Rk += Pl + Pr + Pu + Pd

      move = choose([Pu, Pd, Pl, Pr])

      assert Pu > 0 or move != 0
      assert Pd > 0 or move != 1
      assert Pl > 0 or move != 2
      assert Pr > 0 or move != 3

      if move == 0:
        Bmap[bears[bi]] -= 1
        bears[bi] = (bears[bi][0] - 1, bears[bi][1])
        Bmap[bears[bi]] += 1
      elif move == 1:
        Bmap[bears[bi]] -= 1
        bears[bi] = (bears[bi][0] + 1, bears[bi][1])
        Bmap[bears[bi]] += 1
      elif move == 2:
        Bmap[bears[bi]] -= 1
        bears[bi] = (bears[bi][0], bears[bi][1] - 1)
        Bmap[bears[bi]] += 1
      elif move == 3:
        Bmap[bears[bi]] -= 1
        bears[bi] = (bears[bi][0], bears[bi][1] + 1)
        Bmap[bears[bi]] += 1

    process(bears, k, Rk)


# Utility functions below

def timeInterval(Rk):
  return -log(np.random.rand()) / Rk

# Heaviside function
def H(x):
  if x >= 0:
    return 1
  return 0

# pre: reduce(add, Plist) <= 1
def choose(Plist):
  if Plist == []:
    return -1
  choice = np.random.uniform()
  for i in range(len(Plist)):
    if choice < Plist[i]:
      return i
    choice -= Plist[i]
  return -1

def getBmap(bears):
  Bmap = np.zeros([n,m], 'i')
  for b in bears:
    Bmap[b] += 1
  return Bmap

def l2dist(i, j):
  return ((i[0]-j[0])**2 + (i[1]-j[1])**2)**.5

# Potential well, center, radius, slope
def addLinearWell(PP, i, r, a):
  for j in [(x,y) for x in range(n) for y in range(m)]:
    d = l2dist(i,j)
    if d <= r:
      PP[j] -= a * (r - d)

def addLinearWellLine(PP, start, end, r, a):
  start = np.array(start, 'f')
  end = np.array(end, 'f')
  dse = l2dist(start, end)
  unitdiff = (end - start) / dse
  for j in [(x,y) for x in range(n) for y in range(m)]:
    jt = np.array(j,'f') - start
    proj = jt.dot(unitdiff)
    d=0
    if proj <= 0:
      d = l2dist(start, j)
    elif proj<= dse:
      orth = jt - proj * unitdiff
      d = orth.dot(orth) ** 0.5
    else:
      d = l2dist(end, j)
    if d <= r:
      PP[j] -= a * (r - d)

def colormap(i):
  colormap = ['\033[022m\033[39m', '\033[1m\033[32m', '\033[1m\033[31m', '\033[1m\033[35m', '\033[1m\033[34m']
  if i<len(colormap):
    return colormap[i]
  else:
    return colormap[-1]

def symbolmap(bears, potential):
  head = '.x*'
  heightmap = " .,-'^\"*%$#"
  if bears == 0:
    if (PP.max()-PP.min()) == 0:
      return head[0]
    i = int( len (heightmap) * (potential-PP.min()) / (PP.max()-PP.min())) 
    i = i if i < len(heightmap) else len(heightmap)-1
    return heightmap[i]
  elif bears < len(head):
    return head[bears]
  else: 
    return str(bears)

def prettyprint(bears):
  Bmap = getBmap(bears)
  for i in range(n):
    for j in range(m):
      print colormap(Bmap[i,j]) + symbolmap(Bmap[i,j], PP[i,j]),
    print

if __name__ == "__main__":
  main()

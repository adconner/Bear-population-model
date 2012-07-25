#!/usr/bin/python2

import numpy as np
import time
import string

n = 21 # rows
m = 21 # columns
v = 0.002 # bear velocity (cycles/bears)
N = 10000 # number of time cycles
Bn = 100 # number of bears

# todo: add random walk element? potential function (easily implemented in dead bear units)

# fundamental function of model, compute probability of move to new square
def Pmove(Nfrom, Nto, Bmap):
  return v * (Nfrom - Nto) * H(Nfrom - Nto)

bearmaxinit=3
# return list of tuples of initial bear locations
def initialize():
  # return [(np.random.random_integers(n)-1, np.random.random_integers(m)-1) for num in range(Bn)]
  return [(10,10) for num in range(Bn)]

def process(bears, k):
  print k
  prettyprint(bears)
  time.sleep(0.01)

def main():
  # get initial bear locations
  bears = initialize()

  # initialize bear map
  Bmap = getBmap(bears)

  R = []
  for k in range(N):
    R.append(0)
    for bi in range(len(bears)):
      Pu = Pd = Pl = Pr = 0
      if bears[bi][0]>0:
        Pu = Pmove(Bmap[bears[bi]], Bmap[ bears[bi][0] - 1, bears[bi][1] ], Bmap)
      if bears[bi][0]<n-1:
        Pd = Pmove(Bmap[bears[bi]], Bmap[ bears[bi][0] + 1, bears[bi][1] ], Bmap)
      if bears[bi][1]>0:
        Pl = Pmove(Bmap[bears[bi]], Bmap[ bears[bi][0], bears[bi][1] - 1 ], Bmap)
      if bears[bi][1]<m-1:
        Pr = Pmove(Bmap[bears[bi]], Bmap[ bears[bi][0], bears[bi][1] + 1 ], Bmap)

      R[k] += Pl + Pr + Pu + Pd

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

    process(bears, k)

  return R


# Utility functions below

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

def colormap(i):
  colormap = ['\033[022m\033[39m', '\033[1m\033[32m', '\033[1m\033[31m', '\033[1m\033[35m', '\033[1m\033[34m']
  if i<len(colormap):
    return colormap[i]
  else:
    return colormap[-1]

def symbolmap(i):
  head = '.x*'
  if i < len(head):
    return head[i]
  else: 
    return str(i)

def prettyprint(bears):
  Bmap = getBmap(bears)
  for i in range(n):
    for j in range(m):
      print colormap(Bmap[i,j]) + symbolmap(Bmap[i,j]),
    print


if __name__ == "__main__":
  main()

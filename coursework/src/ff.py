"""
This module contains fitness functions.
"""
import numpy as np

def onemax(array, data=None):
  return sum(array)

def trap5(array, data=None):
  assert(len(array) % 5 == 0)
  fit = 0
  for arr in np.split(np.array(array), int(len(array) / 5)):
    u = sum(arr)
    if u < 5:
      fit += 4 - u
    else:
      fit += 5
  return fit

def invtrap5(array, data=None):
  assert(len(array) % 5 == 0)
  fit = 0
  for arr in np.split(np.array(array), int(len(array) / 5)):
    u = sum(arr)
    if u > 0:
      fit += u - 1
    else:
      fit += 5
  return fit

def sphere(array, data=None):
  return sum([u ** 2 for u in array])

def rosen(array, data=None):
  sum = 0
  for i, u in enumerate(array[:-1]):
    sum += 100 * pow(pow(u, 2) - array[i + 1], 2) + pow(u - 1, 2)
  return sum

def onemax_goal(array):
  return len(array)

def trap5_goal(array):
  assert(len(array) % 5 == 0)
  return len(array)

def invtrap5_goal(array):
  assert(len(array) % 5 == 0)
  return len(array)

def sphere_goal(array):
  return 0

def rosen_goal(array):
  return 0

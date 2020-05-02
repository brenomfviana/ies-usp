"""
This module contains utilitary functions.
"""
import math

def round_up(n, decimals=10):
  multiplier = 10 ** decimals
  return math.floor(n * multiplier) / multiplier

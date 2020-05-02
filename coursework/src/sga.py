"""
This module contains sGA functions to override the run function of pyeasyga.
"""
import sys
import numpy as np

# Run sGA for binary problems
def runb(self, hmdata, multi=False):
  # Create initial population
  self.create_first_generation()
  #
  # Initial Covariance Matrix
  arrs = [np.transpose(i.genes) for i in self.current_generation]
  hmdata['i'] = np.cov(arrs)
  #
  # Run `i` generations
  for i in range(1, self.generations):
    # Create next population
    self.create_next_generation()
    #
    # Intermediary
    if i == int(self.generations / 2):
      # Intermediary Covariance Matrix
      arrs = [np.transpose(i.genes) for i in self.current_generation]
      hmdata['t'] = np.cov(arrs)
  #
  # Final Covariance Matrix
  arrs = [np.transpose(i.genes) for i in self.current_generation]
  hmdata['f'] = np.cov(arrs)

# Run sGA for real numbers problems
def runr(self, hmdata, multi=False):
  pass

"""
This module contains cGA functions to override the run function of pyeasyga.
"""
import sys, random
from pyeasyga import pyeasyga
import numpy as np
from . import sort

# Update probability vector (for monobjective approach)
def update_prob_mono(winner, loser, prob, popsize):
  for i in range(0, len(prob)):
    if winner[i] != loser[i]:
      if winner[i] == 1:
        prob[i] += 1.0 / float(popsize)
      else:
        prob[i] -= 1.0 / float(popsize)

# Create a new individual (for monobjective approach)
def create_individual_mono(prob):
  individual = []
  for p in prob:
    if random.random() < p:
      individual.append(1)
    else:
      individual.append(0)
  return pyeasyga.Chromosome(individual)

# Make competition between two individuals (for monobjective approach)
def compete_mono(a, b):
  if a.fitness > b.fitness:
    return a, b
  else:
    return b, a

# Run cGA for binary problems
def runb(self, hmdata, maximise=True, multi=False):
  # Initialize probability vector
  prob = [0.5] * len(self.seed_data)
  # Initialize best solution
  best = None
  # Population
  population = []
  arrs = []
  #
  # Run `i` generations
  for i in range(0, self.generations):
    # Create individuals
    a = self.create_individual(prob)
    b = self.create_individual(prob)
    #
    # Calculate fitness for each individual
    a.fitness = self.fitness_function(a.genes)
    b.fitness = self.fitness_function(b.genes)
    population.append(a)
    population.append(b)
    #
    # Update best individuals population
    population.sort(key=sort.get_key, reverse=maximise)
    population = population[:self.population_size]
    #
    # Get the best and worst individual
    winner, loser = compete_mono(a, b)
    # Update best solution
    if best:
      if winner.fitness > best.fitness:
        best = winner
    else:
      best = winner
    #
    # Initial population
    if i == 0:
      # Initial Covariance Matrix
      arrs = [np.transpose(i.genes) for i in population]
      hmdata['i'] = np.cov(arrs)
    #
    # Intermediary
    if i == int(self.generations / 2):
      # Intermediary Covariance Matrix
      arrs = [np.transpose(i.genes) for i in population]
      hmdata['t'] = np.cov(arrs)
    #
    # Update the probability vector based on the success of each bit
    update_prob_mono(winner.genes, loser.genes, prob, self.population_size)
  #
  # Add final solution
  self.current_generation.append(best)
  #
  # Final Covariance Matrix
  arrs = [np.transpose(i.genes) for i in population]
  hmdata['f'] = np.cov(arrs)

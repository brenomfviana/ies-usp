"""
This module contains cGA functions to override the run function of pyeasyga.
"""
import sys, random
from pyeasyga import pyeasyga
import numpy as np
from .ff import ERR
from . import sort, utils

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
    winner, loser = bn_compete(a, b)
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
    bn_update_prob(winner.genes, loser.genes, prob, self.population_size)
  #
  # Add final solution
  self.current_generation.append(best)
  #
  # Final Covariance Matrix
  arrs = [np.transpose(i.genes) for i in population]
  hmdata['f'] = np.cov(arrs)


# Update probability vector (for monobjective approach)
def bn_update_prob(winner, loser, prob, popsize):
  for i in range(0, len(prob)):
    if winner[i] != loser[i]:
      if winner[i] == 1:
        prob[i] += 1.0 / float(popsize)
      else:
        prob[i] -= 1.0 / float(popsize)

# Create a new individual (for monobjective approach)
def bn_create_individual(prob):
  individual = []
  for p in prob:
    if random.random() < p:
      individual.append(1)
    else:
      individual.append(0)
  return pyeasyga.Chromosome(individual)

# Make competition between two individuals (for monobjective approach)
def bn_compete(a, b):
  if a.fitness > b.fitness:
    return a, b
  else:
    return b, a



def runr(self, hmdata, maximise=True, multi=False):
  # Initialize the max number of individuals in a offspring
  offspring_max = self.population_size
  # Initialize best solution
  best = None
  # Initialize best individuals population
  k = int(self.population_size / 2)
  population = []
  arrs = []
  #
  # Initialize probability vector
  prob = rn_generate_prob(len(self.seed_data))
  #
  # Run `i` generations
  for i in range(self.generations):
    # Create individuals
    for _ in range(offspring_max):
      downward = self.create_individual(prob)
      downward.fitness = utils.round_up(self.fitness_function(downward.genes))
      downward.fitness = 0 if ERR >= downward.fitness else downward.fitness
      population.append(downward)
    #
    # Update best individuals population
    population.sort(key=sort.get_key)
    population = population[:self.population_size]
    elite = population[:k]
    best = population[0]
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
    rn_update_prob(elite, prob)
  #
  # Add final solution
  self.current_generation.append(best)
  #
  # Update best individuals population
  population.sort(key=sort.get_key)
  population = population[:self.population_size]
  #
  # Final Covariance Matrix
  arrs = [np.transpose(i.genes) for i in population]
  hmdata['f'] = np.cov(arrs)


# Generate probability vector
def rn_generate_prob(model_size):
  prob = []
  std_stdev = 1
  for i in range(model_size):
    bound = model_size + std_stdev
    mean = random.uniform(-bound, bound)
    pair = (mean, std_stdev)
    prob.append(pair)
  return prob

# Update probability vector
def rn_update_prob(elite, prob):
  # Update probability vector with the best results
  for i in range(len(prob)):
    # Mean and standard deviation of the ith element
    aux = []
    for item in elite:
      mean = item.genes[i]
      aux.append(mean)
    # Update mean and stdev
    prob[i] = np.mean(aux), np.std(aux, ddof=1)

# Create a new individual
def rn_create_individual(prob):
  individual = []
  for (mean, stdev) in prob:
    value = random.uniform(mean - stdev, mean + stdev)
    individual.append(value)
  mean = np.mean(individual)
  stdev = np.std(individual, ddof=1)
  individual = np.random.normal(mean, stdev, len(individual))
  # Return a new individual
  return pyeasyga.Chromosome(individual)

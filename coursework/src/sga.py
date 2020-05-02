"""
This module contains sGA functions to override the run function of pyeasyga.
"""
import sys
import random
import numpy as np
from .ff import ERR
from . import utils

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
  for i in range(self.generations):
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
  # Initialize seed data with random values
  model_size = len(self.seed_data)
  for i in range(model_size):
    self.seed_data[i] = random.uniform(0, model_size)
  #
  # Create initial population
  self.create_first_generation(self)
  #
  # Initial Covariance Matrix
  arrs = [np.transpose(i.genes) for i in self.current_generation]
  hmdata['i'] = np.cov(arrs)
  #
  # Run `i` generations
  for i in range(self.generations):
    # Create next population
    self.create_next_generation(self)
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


# Create a new individual
def rn_create_individual(data):
  # Set mutation range
  mrange = len(data)
  # Generate a random individual
  individual = []
  for d in data:
    individual.append(random.uniform(d - mrange, d + mrange))
  # Return a new individual
  return individual

# Fix mutate function
def rn_mutate_function(individual):
  # Set mutation range
  mrange = max(individual)
  mutate_index = random.randrange(len(individual))
  d = individual[mutate_index]
  individual[mutate_index] = random.uniform(d - mrange, d + mrange)

# Fix population fitness calculation
def rn_calculate_population_fitness(self):
  for individual in self.current_generation:
    individual.fitness = self.fitness_function(individual.genes, self.seed_data)
    individual.fitness = utils.round_up(individual.fitness)
    individual.fitness = 0 if ERR >= individual.fitness else individual.fitness

# Set initial population generation function (fix rank population call)
def rn_create_first_generation(self):
  self.create_initial_population()
  self.calculate_population_fitness(self)
  self.rank_population()

# Set next population generation function (fix rank population call)
def rn_create_next_generation(self):
  self.create_new_population()
  self.calculate_population_fitness(self)
  self.rank_population()

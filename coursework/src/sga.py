"""
This module contains sGA functions to override the run function of pyeasyga.
"""
import sys
import random
import numpy as np
from .ff import ERR
from . import sort, utils


# Set initial population generation function (fix rank population call)
def create_first_generation(self, multi=False):
  self.create_initial_population()
  self.calculate_population_fitness(self, multi)
  self.rank_population(self, multi)

# Set next population generation function (fix rank population call)
def create_next_generation(self, multi=False):
  self.create_new_population()
  self.calculate_population_fitness(self, multi)
  self.rank_population(self, multi)

def best_individual(self, multi=False):
  if multi:
    return [(a.fitness, a.genes) for a in self.current_generation[0]]
  else:
    best = self.current_generation[0]
    return [best.fitness, best.genes]

# Set rank population function (now it uses NSGA-II algorithm)
def rank_population(self, multi=False):
  if multi:
    self.current_generation = sort.nsgaii(self.current_generation,
      maximise=self.maximise_fitness)
  else:
    self.current_generation.sort(key=sort.get_key,
      reverse=self.maximise_fitness)



# Run sGA for binary problems
def bn_run(self, hmdata, multi=False):
  # Create initial population
  self.create_first_generation(self, multi)
  #
  # Initial Covariance Matrix
  arrs = [np.transpose(i.genes) for i in self.current_generation]
  hmdata['i'] = np.cov(arrs)
  #
  # Run `i` generations
  for i in range(self.generations):
    # Create next population
    self.create_next_generation(self, multi)
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
  #
  # Add final solution
  if multi:
    indexes = sort.nsgaii_select(self.current_generation, self.maximise_fitness)
    nondominated = []
    for i in indexes:
      nondominated.append(self.current_generation[i])
    self.current_generation.clear()
    self.current_generation.append(nondominated)
  else:
    best = self.current_generation[0]
    self.current_generation.clear()
    self.current_generation.append(best)


# Fix population fitness calculation
def bn_calculate_population_fitness(self, multi=False):
  if multi:
    f_a, f_b = self.fitness_function
    for individual in self.current_generation:
      fit_a = f_a(individual.genes, self.seed_data)
      fit_b = f_b(individual.genes, self.seed_data)
      individual.fitness = (fit_a, fit_b)
  else:
    for individual in self.current_generation:
      fitness = self.fitness_function(individual.genes, self.seed_data)
      individual.fitness = fitness



# Run sGA for real numbers problems
def rn_run(self, hmdata, multi=False):
  # Initialize seed data with random values
  model_size = len(self.seed_data)
  bound = int(model_size * 0.05)
  for i in range(model_size):
    self.seed_data[i] = random.uniform(0, bound)
  #
  # Create initial population
  self.create_first_generation(self, multi)
  #
  # Initial Covariance Matrix
  arrs = [np.transpose(i.genes) for i in self.current_generation]
  hmdata['i'] = np.cov(arrs)
  #
  # Run `i` generations
  for i in range(self.generations):
    # Create next population
    self.create_next_generation(self, multi)
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
  #
  # Add final solution
  if multi:
    indexes = sort.nsgaii_select(self.current_generation, self.maximise_fitness)
    nondominated = []
    for i in indexes:
      nondominated.append(self.current_generation[i])
    self.current_generation.clear()
    self.current_generation.append(nondominated)
  else:
    best = self.current_generation[0]
    self.current_generation.clear()
    self.current_generation.append(best)


# Create a new individual
def rn_create_individual(data):
  # Set mutation range
  mrange = len(data)
  # Generate a random individual
  individual = []
  for d in data:
    individual.append(random.uniform(d - mrange, d + mrange))
  mean = np.mean(individual)
  stdev = np.std(individual, ddof=1)
  individual = np.random.normal(mean, stdev, mrange).tolist()
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
def rn_calculate_population_fitness(self, multi=False):
  if multi:
    f_a, f_b = self.fitness_function
    for individual in self.current_generation:
      # Calculate `a` fitness
      fit_a = f_a(individual.genes, self.seed_data)
      fit_a = utils.round_up(fit_a)
      fit_a = 0 if ERR >= fit_a else fit_a
      # Calculate `b` fitness
      fit_b = f_b(individual.genes, self.seed_data)
      fit_b = utils.round_up(fit_b)
      fit_b = 0 if ERR >= fit_b else fit_b
      # Join
      individual.fitness = (fit_a, fit_b)
  else:
    for individual in self.current_generation:
      fitness = self.fitness_function(individual.genes, self.seed_data)
      fitness = utils.round_up(fitness)
      fitness = 0 if ERR >= fitness else fitness
      individual.fitness = fitness

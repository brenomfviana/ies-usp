from pyeasyga import pyeasyga
from . import sga, cga, charts

def mono_binary(function, goal_function, size, popsz, noe, maximise=True):
  # Define data
  data = [0] * size
  #
  # Save the fitness of each execution
  results_sga = []
  hmdatas_sga = []
  # Execute the sGA `noe` times (noe: number of executions)
  for _ in range(noe):
    # Heat map data
    hmdata = {}
    # Set sGA
    ga = pyeasyga.GeneticAlgorithm(data, population_size=popsz,
      maximise_fitness=maximise)
    ga.fitness_function = function
    ga.run = sga.runb
    # Run binary sGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual()
    # Update extraction variables
    results_sga.append(fitness)
    hmdatas_sga.append(hmdata)
  #
  # Save the fitness of each execution
  results_cga = []
  hmdatas_cga = []
  # Execute the cGA `noe` times (noe: number of executions)
  for _ in range(noe):
    # Heat map data
    hmdata = {}
    # Set cGA
    ga = pyeasyga.GeneticAlgorithm(data, population_size=popsz,
      maximise_fitness=maximise)
    ga.fitness_function = function
    ga.create_individual = cga.bn_create_individual
    ga.run = cga.runb
    # Run binary cGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual()
    # Update extraction variables
    results_cga.append(fitness)
    hmdatas_cga.append(hmdata)
  #
  # Get goal of the fitness function
  goal = goal_function(data)
  #
  # Plot result charts
  filename = function.__name__ + '_' + str(size) + '_' + str(popsz)
  charts.results(results_sga, results_cga, popsz, goal, noe, filename)
  # Plot heat map charts
  for i, _ in enumerate(hmdatas_sga):
    charts.heat_map(hmdatas_sga[i], hmdatas_cga[i], filename, i + 1)



def mono_real(function, goal_function, size, popsz, noe, maximise=False):
  # Define data
  data = [0] * size
  #
  # Save the fitness of each execution
  results_sga = []
  hmdatas_sga = []
  # Execute the sGA `noe` times (noe: number of executions)
  for _ in range(noe):
    # Heat map data
    hmdata = {}
    # Set sGA
    ga = pyeasyga.GeneticAlgorithm(data, population_size=popsz,
      maximise_fitness=maximise)
    ga.fitness_function = function
    # Update default functions
    ga.create_individual = sga.rn_create_individual
    ga.mutate_function = sga.rn_mutate_function
    ga.create_first_generation = sga.rn_create_first_generation
    ga.create_next_generation = sga.rn_create_next_generation
    ga.calculate_population_fitness = sga.rn_calculate_population_fitness
    # Run real sGA
    ga.run = sga.runr
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual()
    # Update extraction variables
    results_sga.append(fitness)
    hmdatas_sga.append(hmdata)
  #
  # Save the fitness of each execution
  results_cga = []
  hmdatas_cga = []
  # Execute the cGA `noe` times (noe: number of executions)
  for _ in range(noe):
    # Heat map data
    hmdata = {}
    # Set cGA
    ga = pyeasyga.GeneticAlgorithm(data, population_size=popsz,
      maximise_fitness=maximise)
    ga.fitness_function = function
    ga.create_individual = cga.rn_create_individual
    ga.run = cga.runr
    # Run real cGA
    ga.run(ga, hmdata, )
    # Get best individual
    fitness, _ = ga.best_individual()
    # Update extraction variables
    results_cga.append(fitness)
    hmdatas_cga.append(hmdata)
  #
  # Get goal of the fitness function
  goal = goal_function(data)
  #
  # Plot result charts
  filename = function.__name__ + '_' + str(size) + '_' + str(popsz)
  charts.results(results_sga, results_cga, popsz, goal, noe, filename)
  # Plot heat map charts
  for i, _ in enumerate(hmdatas_sga):
    charts.heat_map(hmdatas_sga[i], hmdatas_cga[i], filename, i + 1)



def multi_binary():
  pass



def multi_real():
  pass

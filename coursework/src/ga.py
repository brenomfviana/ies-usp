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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.create_first_generation = sga.create_first_generation
    ga.create_next_generation = sga.create_next_generation
    ga.best_individual = sga.best_individual
    ga.rank_population = sga.rank_population
    ga.calculate_population_fitness = sga.bn_calculate_population_fitness
    ga.run = sga.bn_run
    # Run binary sGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual(ga)
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.best_individual = cga.best_individual
    ga.create_individual = cga.bn_create_individual
    ga.run = cga.bn_run
    # Run binary cGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual(ga)
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.create_first_generation = sga.create_first_generation
    ga.create_next_generation = sga.create_next_generation
    ga.best_individual = sga.best_individual
    ga.rank_population = sga.rank_population
    ga.create_individual = sga.rn_create_individual
    ga.mutate_function = sga.rn_mutate_function
    ga.calculate_population_fitness = sga.rn_calculate_population_fitness
    ga.run = sga.rn_run
    # Run real sGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual(ga)
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.best_individual = cga.best_individual
    ga.create_individual = cga.rn_create_individual
    ga.run = cga.rn_run
    # Run real cGA
    ga.run(ga, hmdata)
    # Get best individual
    fitness, _ = ga.best_individual(ga)
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



def multi_binary(function, goal_function, size, popsz, noe, maximise=True):
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.create_first_generation = sga.create_first_generation
    ga.create_next_generation = sga.create_next_generation
    ga.best_individual = sga.best_individual
    ga.rank_population = sga.rank_population
    ga.calculate_population_fitness = sga.bn_calculate_population_fitness
    ga.run = sga.bn_run
    # Run binary sGA
    ga.run(ga, hmdata, multi=True)
    # Get best individual
    nondominated = ga.best_individual(ga, multi=True)
    nddata = []
    for nd in nondominated:
      # Update extraction variables
      fitness, _ = nd
      nddata.append(fitness)
    results_sga.append(nddata)
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.best_individual = cga.best_individual
    ga.create_individual = cga.bn_create_individual
    ga.run = cga.bn_run
    # Run binary cGA
    ga.run(ga, hmdata, multi=True)
    # Get best individual
    nondominated = ga.best_individual(ga, multi=True)
    nddata = []
    for nd in nondominated:
      # Update extraction variables
      fitness, _ = nd
      nddata.append(fitness)
    results_cga.append(nddata)
    hmdatas_cga.append(hmdata)
  #
  # Get goal of the fitness function
  fa_goal, fb_goal = goal_function
  goal = fa_goal(data), fb_goal(data)
  #
  # Plot hypervolume charts
  fa, fb = function
  fname = fa.__name__ + '_' + fb.__name__ + '_'
  filename = fname + str(size) + '_' + str(popsz)
  for i, _ in enumerate(results_sga):
    charts.hypervolume(results_sga[i], results_cga[i], goal,
      True, filename, i + 1)
  #
  # Plot heat map charts
  for i, _ in enumerate(hmdatas_sga):
    charts.heat_map(hmdatas_sga[i], hmdatas_cga[i], filename, i + 1)



def multi_real(function, goal_function, size, popsz, noe, maximise=False):
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.create_first_generation = sga.create_first_generation
    ga.create_next_generation = sga.create_next_generation
    ga.best_individual = sga.best_individual
    ga.rank_population = sga.rank_population
    ga.create_individual = sga.rn_create_individual
    ga.mutate_function = sga.rn_mutate_function
    ga.calculate_population_fitness = sga.rn_calculate_population_fitness
    ga.run = sga.rn_run
    # Run real sGA
    ga.run(ga, hmdata, multi=True)
    # Get best individual
    nondominated = ga.best_individual(ga, multi=True)
    nddata = []
    for nd in nondominated:
      # Update extraction variables
      fitness, _ = nd
      nddata.append(fitness)
    results_sga.append(nddata)
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
      maximise_fitness=maximise, generations=200)
    ga.fitness_function = function
    # Update default functions
    ga.best_individual = cga.best_individual
    ga.create_individual = cga.rn_create_individual
    ga.run = cga.rn_run
    # Run real cGA
    ga.run(ga, hmdata, multi=True)
    # Get best individual
    nondominated = ga.best_individual(ga, multi=True)
    nddata = []
    for nd in nondominated:
      # Update extraction variables
      fitness, _ = nd
      nddata.append(fitness)
    results_cga.append(nddata)
    hmdatas_cga.append(hmdata)
  #
  # Get goal of the fitness function
  fa_goal, fb_goal = goal_function
  goal = fa_goal(data), fb_goal(data)
  #
  # Plot hypervolume charts
  fa, fb = function
  fname = fa.__name__ + '_' + fb.__name__ + '_'
  filename = fname + str(size) + '_' + str(popsz)
  for i, _ in enumerate(results_sga):
    charts.hypervolume(results_sga[i], results_cga[i], goal,
      False, filename, i + 1)
  #
  # Plot heat map charts
  for i, _ in enumerate(hmdatas_sga):
    charts.heat_map(hmdatas_sga[i], hmdatas_cga[i], filename, i + 1)

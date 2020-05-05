#!/usr/bin/env python3
import os

# Number of executions
NOE = 100

# Problems
problems = [
  # Binary
  'onemax', 'trap5', 'invtrap5',
  # Real
  'sphere', 'rosen',
  # Multi binary
  'multibi',
  # Multi real
  'multirn'
]

# Problem sizes
problem_sizes = [10, 20, 40, 80, 160]

# Population sizes
population_sizes = [10, 20, 40, 80, 160]

# Run algorithms
for posz in population_sizes:
  for prsz in problem_sizes:
    for pr in problems:
      args = pr + ' ' + str(prsz) + ' ' + str(posz) + ' ' + str(NOE)
      os.system('python main.py ' + args)

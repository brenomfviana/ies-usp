#!/usr/bin/env python3

"""
This module redirects the function call according to the problem to be solved.
"""

import sys
from src import ga, ff

def run(problem, problem_size, population_size, noe):
  if problem == 'onemax':
    ga.mono_binary(ff.onemax, ff.onemax_goal,
      problem_size, population_size, noe)
  if problem == 'trap5':
    ga.mono_binary(ff.trap5, ff.trap5_goal,
      problem_size, population_size, noe)
  if problem == 'invtrap5':
    ga.mono_binary(ff.invtrap5, ff.invtrap5_goal,
      problem_size, population_size, noe)
  if problem == 'sphere':
    ga.mono_real(ff.sphere, ff.sphere_goal,
      problem_size, population_size, noe)
  if problem == 'rosen':
    ga.mono_real(ff.rosen, ff.rosen_goal,
      problem_size, population_size, noe)
  if problem == 'multibi':
    ga.multi_binary((ff.trap5, ff.invtrap5), (ff.trap5_goal, ff.invtrap5_goal),
      problem_size, population_size, noe)
  if problem == 'multirn':
    ga.multi_real((ff.sphere, ff.rosen), (ff.sphere_goal, ff.rosen_goal),
      problem_size, population_size, noe)

if __name__ == '__main__':
  problem = sys.argv[1]
  problem_size = int(sys.argv[2])
  population_size = int(sys.argv[3])
  noe = int(sys.argv[4])
  run(problem, problem_size, population_size, noe)

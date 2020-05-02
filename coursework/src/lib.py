"""
This module redirects the function call according to the problem to be solved.
"""
from . import ga, ff

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
  # if problem == 'sphere':
  #   ff.sphere
  # if problem == 'rosen':
  #   ff.rosen
  # if problem == 'multibi':
  #   ff.trap5, ff.invtrap5
  # if problem == 'multirn':
  #   ff.sphere, ff.rosen
  # print(problem, problem_size, population_size)

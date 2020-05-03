"""
This module contains sort-related functions.
"""

# Define the key field for sorting
def get_key(obj):
  return obj.fitness

# Sort function: fast non-dominated sort
def nsgaii(population, maximise):
  # Get population size
  popsize = len(population)
  poprange = range(popsize)
  #
  # Initialize the sorted population
  front = [[]]
  # Initialize the set of solutions that are dominated
  s = [[] for i in poprange]
  # Initialize the number of solutions which dominate an individual
  n = [0 for i in poprange]
  # Initialize the rank of solutions
  rank = [0 for i in poprange]
  #
  # Looks for the `p`-dominated solutions and
  # calculates the degree of domination over `p`
  for p in poprange:
    s[p] = []
    n[p] = 0
    # Get `p` fitness
    pfa, pfb = population[p].fitness
    for q in poprange:
      # Get `q` fitness
      qfa, qfb = population[q].fitness
      #
      # Maximise `p` domination
      if maximise:
        # Check which dominates which
        if ((pfa > qfa and pfb > qfb) or (pfa >= qfa and pfb > qfb)
          or (pfa > qfa and pfb >= qfb)):
            s[p].append(q)
        elif ((qfa > pfa and qfb > pfb) or (qfa >= pfa and qfb > pfb)
          or (qfa > pfa and qfb >= pfb)):
            n[p] += 1
      #
      # Minimise `p` domination
      else:
        # Check which dominates which
        if ((pfa < qfa and pfb < qfb) or (pfa <= qfa and pfb < qfb)
          or (pfa < qfa and pfb <= qfb)):
            s[p].append(q)
        elif ((qfa < pfa and qfb < pfb) or (qfa <= pfa and qfb < pfb)
          or (qfa < pfa and qfb <= pfb)):
            n[p] += 1
    #
    # Check if `p` belongs to the fisrt front
    if n[p] == 0:
      rank[p] = 0
      if p not in front[0]:
        front[0].append(p)
  #
  # Initiliaze the front counter
  i = 0
  while front[i] != []:
    aux = []
    for p in front[i]:
      for q in s[p]:
        n[q] = n[q] - 1
        if n[q] == 0:
          rank[q] = i + 1
          if q not in aux:
            aux.append(q)
    i += 1
    front.append(aux)
  # Remove the last set of individuals
  del front[len(front) - 1]
  #
  # Convert to a usual population list
  sorted_pop = []
  for f in front:
    for i in f:
      sorted_pop.append(population[i])
  return sorted_pop

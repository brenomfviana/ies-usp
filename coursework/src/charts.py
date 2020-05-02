"""
This module contains function to plot chats.
"""
import os
import sys
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
plt.style.use('ggplot')

ROOT_PATH = 'results'
RESULT_PATH = 'results/sgavscga'
HEATMAP_PATH = 'results/heatmap'
HYPERPLANE_PATH = 'results/hyperplane'

def _fmt(x, pos):
  return r'{:.2f}'.format(x)

def _create_folders():
  if not os.path.isdir(ROOT_PATH):
    os.mkdir(ROOT_PATH)
  if not os.path.isdir(RESULT_PATH):
    os.mkdir(RESULT_PATH)
  if not os.path.isdir(HEATMAP_PATH):
    os.mkdir(HEATMAP_PATH)
  if not os.path.isdir(HYPERPLANE_PATH):
    os.mkdir(HYPERPLANE_PATH)

def results(results_sga, results_cga, population_size, goal, noe, filename):
  _create_folders()
  # Calculate sGA accuracy
  sga_accuracy = 0.0
  for f in results_sga:
    sga_accuracy += 1 if f == goal else 0
  sga_accuracy /= noe
  # Calculate cGA accuracy
  cga_accuracy = 0.0
  for f in results_cga:
    cga_accuracy += 1 if f == goal else 0
  cga_accuracy /= noe
  # Plot
  fig = plt.figure()
  fig.suptitle('População de ' + str(population_size) + ' indivíduos',
     fontsize=14, fontweight='bold')
  line_sga, = plt.plot(results_sga)
  line_cga, = plt.plot(results_cga)
  plt.ylim(0, 20)
  plt.legend([line_sga, line_cga],
    ['sGA ({:.2f}%)'.format(sga_accuracy * 100),
     'cGA ({:.2f}%)'.format(cga_accuracy * 100)])
  plt.xlabel('Execuções')
  plt.ylabel('Fitness')
  plt.savefig(RESULT_PATH + '/' + filename + '.png')

def heat_map(hmsga, hmcga, filename, i):
  # Set bounds
  hmmin, hmmax = -0.3, 0.3
  # max(max(fitness_sga[i]), max(fitness_cga[i]))
  # Create folder
  foldername = HEATMAP_PATH + '/' + filename
  if not os.path.isdir(foldername):
    os.mkdir(foldername)
  #
  # sGA
  # Initial population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('sGA\nMatriz de Covariância da População Inicial',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmsga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('sGA\nMatriz de Covariância da População Intermediária',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmsga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('sGA\nMatriz de Covariância da População Final',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmsga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_c' + '.png')
  #
  # cGA
  # Initial population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('cGA\nMatriz de Covariância da População Inicial',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmcga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('cGA\nMatriz de Covariância da População Intermediária',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmcga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(13, 10))
  fig.suptitle('cGA\nMatriz de Covariância da População Final',
    fontsize=14, fontweight='bold', y=0.94)
  heatmap = axis.pcolor(hmcga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_c' + '.png')

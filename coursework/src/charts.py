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
  # Create result folders
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
     fontsize=12, fontweight='bold')
  line_sga, = plt.plot(results_sga)
  line_cga, = plt.plot(results_cga, linestyle='--')
  plt.ylim(0, max(max(results_sga) * 1.2, max(results_cga) * 1.2, goal * 1.2))
  plt.legend([line_sga, line_cga],
    ['sGA ({:.2f}%)'.format(sga_accuracy * 100),
     'cGA ({:.2f}%)'.format(cga_accuracy * 100)])
  plt.xlabel('Execuções')
  plt.ylabel('Fitness')
  plt.savefig(RESULT_PATH + '/' + filename + '.png')

def heat_map(hmsga, hmcga, filename, i):
  # Create result folders
  _create_folders()
  # Set bounds
  hmmin, hmmax = sys.float_info.max, sys.float_info.min
  for cvm in hmsga.values():
    for arr in cvm:
      hmmin = min(hmmin, min(arr))
      hmmax = max(hmmax, max(arr))
  for cvm in hmcga.values():
    for arr in cvm:
      hmmin = min(hmmin, min(arr))
      hmmax = max(hmmax, max(arr))
  # max(max(fitness_sga[i]), max(fitness_cga[i]))
  # Create folder
  foldername = HEATMAP_PATH + '/' + filename
  if not os.path.isdir(foldername):
    os.mkdir(foldername)
  #
  # sGA
  # Initial population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('sGA\nMatriz de Covariância da População Inicial',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('sGA\nMatriz de Covariância da População Intermediária',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('sGA\nMatriz de Covariância da População Final',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_sga_c' + '.png')
  #
  # cGA
  # Initial population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('cGA\nMatriz de Covariância da População Inicial',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('cGA\nMatriz de Covariância da População Intermediária',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  fig.suptitle('cGA\nMatriz de Covariância da População Final',
    fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  plt.savefig(foldername + '/' + str(i) + '_cga_c' + '.png')

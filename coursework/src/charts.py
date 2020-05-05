"""
This module contains function to plot chats.
"""
import os
import sys
import math
import numpy as np
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
plt.style.use('ggplot')

ROOT_PATH = 'results'
RESULT_PATH = 'results/sgavscga'
HEATMAP_PATH = 'results/heatmap'
HYPERVOLUME_PATH = 'results/hypervolume'

def _fmt(x, pos):
  return r'{:.2f}'.format(x)

def _create_folders():
  if not os.path.isdir(ROOT_PATH):
    os.mkdir(ROOT_PATH)
  if not os.path.isdir(RESULT_PATH):
    os.mkdir(RESULT_PATH)
  if not os.path.isdir(HEATMAP_PATH):
    os.mkdir(HEATMAP_PATH)
  if not os.path.isdir(HYPERVOLUME_PATH):
    os.mkdir(HYPERVOLUME_PATH)


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
  fig, axes = plt.subplots(figsize=(12.8, 4.8))
  # fig.suptitle('População de ' + str(population_size) + ' indivíduos',
  #    fontsize=12, fontweight='bold')
  plot_sga = [a for a in enumerate(results_sga, 1)]
  plot_cga = [a for a in enumerate(results_cga, 1)]
  line_sga, = plt.plot(*zip(*plot_sga))
  line_cga, = plt.plot(*zip(*plot_cga), linestyle=':', color='blue', alpha=0.5)
  plt.xlim(1, noe)
  plt.ylim(0, max(max(results_sga) * 1.2, max(results_cga) * 1.2, goal * 1.2))
  nexe = np.arange(0, noe + 1, 5)
  plt.xticks(nexe)
  plt.legend([line_sga, line_cga],
    ['sGA ({:.2f}%)'.format(sga_accuracy * 100),
     'cGA ({:.2f}%)'.format(cga_accuracy * 100)])
  plt.xlabel('Execuções')
  plt.ylabel('Fitness')
  fig.tight_layout()
  plt.savefig(RESULT_PATH + '/' + filename + '.png')
  plt.close('all')
  #
  fig, axes = plt.subplots(figsize=(8, 16))
  axes.axis('off')
  axes.axis('tight')
  fig.patch.set_visible(False)
  columns = ('sGA', 'cGA')
  rows = [i for i, a in enumerate(results_sga, 1)]
  content = []
  for i, _ in enumerate(results_sga):
    content.append((results_sga[i], results_cga[i]))
  table = axes.table(cellText=content, colLabels=columns,
    rowLabels=rows, loc='center')
  fig.tight_layout()
  # Sava
  foldername = RESULT_PATH + '/' + 'tables'
  if not os.path.isdir(foldername):
    os.mkdir(foldername)
  plt.savefig(foldername + '/' + filename + '.png')
  plt.close('all')


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
  # fig.suptitle('sGA\nMatriz de Covariância da População Inicial',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_sga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  # fig.suptitle('sGA\nMatriz de Covariância da População Intermediária',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_sga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  # fig.suptitle('sGA\nMatriz de Covariância da População Final',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmsga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Blues)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_sga_c' + '.png')
  #
  # cGA
  # Initial population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  # fig.suptitle('cGA\nMatriz de Covariância da População Inicial',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['i'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_cga_a' + '.png')
  # Intermediary population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  # fig.suptitle('cGA\nMatriz de Covariância da População Intermediária',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['t'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_cga_b' + '.png')
  # Final population heat map
  fig, axis = plt.subplots(figsize=(6.4, 4.8))
  # fig.suptitle('cGA\nMatriz de Covariância da População Final',
  #   fontsize=12, fontweight='bold')
  heatmap = axis.pcolor(hmcga['f'], vmin=hmmin, vmax=hmmax, cmap=plt.cm.Reds)
  plt.colorbar(heatmap, format=ticker.FuncFormatter(_fmt))
  fig.tight_layout()
  plt.savefig(foldername + '/' + str(i) + '_cga_c' + '.png')
  plt.close('all')


def hypervolume(nondominated_sga, nondominated_cga, goal, maximise,
  filename, i):
    # Create result folders
    _create_folders()
    # sGA
    fig, axes = plt.subplots()
    # fig.suptitle('sGA\nHipervolume', fontsize=12, fontweight='bold')
    x, y = goal
    # Get values
    obj1 = [a for a, _ in nondominated_sga]
    obj2 = [b for _, b in nondominated_sga]
    # Plot area
    if maximise:
      for k, _ in enumerate(obj1):
        rect = plt.Rectangle((obj1[k], obj2[k]), x, y, fill=True, linewidth=0,
          facecolor='#8cb7d0')
        plt.gca().add_patch(rect)
      lim = max(x, y)
      plt.xlim(0, lim)
      plt.ylim(0, lim)
    else:
      for k, _ in enumerate(obj1):
        rect = plt.Rectangle((x, y), obj1[k], obj2[k], fill=True, linewidth=0,
          facecolor='#8cb7d0')
        plt.gca().add_patch(rect)
      plt.xlim(0, max(math.ceil(max(obj1) * 1.2), 1))
      plt.ylim(0, max(math.ceil(max(obj2) * 1.2), 1))
    # Print solutions
    axes.scatter(obj1, obj2, color='blue', zorder = 2, clip_on=False)
    axes.scatter(x, y, zorder = 2, color='black', clip_on=False)
    plt.xlabel('$f_1(x)$')
    plt.ylabel('$f_2(x)$')
    # Save
    foldername = HYPERVOLUME_PATH + '/' + filename
    if not os.path.isdir(foldername):
      os.mkdir(foldername)
    plt.savefig(foldername + '/' + str(i) + '_sga_hypervolume' + '.png')
    plt.close('all')
    #
    # cGA
    fig, axes = plt.subplots()
    # fig.suptitle('cGA\nHipervolume', fontsize=12, fontweight='bold')
    x, y = goal
    # Get values
    obj1 = [a for a, _ in nondominated_cga]
    obj2 = [b for _, b in nondominated_cga]
    # Plot area
    if maximise:
      for k, _ in enumerate(obj1):
        rect = plt.Rectangle((obj1[k], obj2[k]), x, y, fill=True, linewidth=0,
          facecolor='#e28c7f')
        plt.gca().add_patch(rect)
      lim = max(x, y)
      plt.xlim(0, lim)
      plt.ylim(0, lim)
    else:
      for k, _ in enumerate(obj1):
        rect = plt.Rectangle((x, y), obj1[k], obj2[k], fill=True, linewidth=0,
          facecolor='#e28c7f')
        plt.gca().add_patch(rect)
      plt.xlim(0, max(math.ceil(max(obj1) * 1.2), 1))
      plt.ylim(0, max(math.ceil(max(obj2) * 1.2), 1))
    # Print solutions
    axes.scatter(obj1, obj2, zorder = 2, clip_on=False)
    axes.scatter(x, y, zorder = 2, color='black', clip_on=False)
    plt.xlabel('$f_1(x)$')
    plt.ylabel('$f_2(x)$')
    # Save
    foldername = HYPERVOLUME_PATH + '/' + filename
    if not os.path.isdir(foldername):
      os.mkdir(foldername)
    plt.savefig(foldername + '/' + str(i) + '_cga_hypervolume' + '.png')
    plt.close('all')

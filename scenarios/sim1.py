from statistics import mean
import random
from numpy import cumsum
from copy import deepcopy
import matplotlib.pyplot as plt

def adjustDifficulty(ls, solveTimes, tgt = 180):
    avg = mean(ls)
    _sum = 0
    denom = 0
    for i in range(0, len(solveTimes)):
        _sum += (solveTimes[i] * (i+1))
        denom += (i+1)
    return avg * (tgt/(_sum/denom))

def probs(_a, _b):
    _probs = [b / m for b,m in zip(_a, _b)]
    _probs = [b/sum(_probs) for b in _probs]
    return _probs

initialDifficulty = int(input('Set initial difficulty of all algorithms: '))
simTime = int(input('Enter simulation time(hours): '))
noAlgos = int(input('Enter the number of mining algorithms: '))

algos = []
for algo in range(0, noAlgos):
    algos.append([input('Assign name to algorithm %d: ' %(algo + 1))])
    
for algo in algos:
    algo.append(int(input('Enter initial hashrate of %s: ' % algo[0])))
    algo.append(initialDifficulty)
    
seconds = simTime * 3600

transposed = list(map(list, zip(*algos)))
_probs = probs(transposed[1], transposed[2])
transposed.append(_probs)
transposed.append([0] * len(transposed[0]))
_empty = []
for i in range(0, len(transposed[0])):
    _empty.append([])
_new = deepcopy(_empty)
transposed.append(_empty)
transposed.append(_new)

_pr = 0.0166667
count = 0
for i in range(0, seconds):
    if(random.uniform(0, 1) < _pr):
        count += 1
        _try = random.uniform(0, 1)
        cum = cumsum(transposed[3])
        for i in range(0, len(transposed[3])):
            if _try < cum[i]:
                transposed[5][i].append(transposed[4][i])
                transposed[6][i].append(transposed[2][i])
                transposed[4][i] = -1
                transposed[2][i] = adjustDifficulty(transposed[6][i], transposed[5][i], 180)
                transposed[3] = probs(transposed[1], transposed[2])
                break
    for i in range(0, len(transposed[4])):
        transposed[4][i] += 1
        
fig, axs = plt.subplots(len(transposed[0]), 2, figsize=(15,15))
fig.subplots_adjust(hspace=0.8, wspace=0.4)
for i in range(0, len(transposed[0])):
    axs[i, 0].plot(transposed[6][i])
    axs[i, 0].set_title(transposed[0][i] + ': difficulty')
    axs[i, 1].plot(transposed[5][i])
    axs[i, 1].set_title(transposed[0][i] + ': Solve time')
plt.show()
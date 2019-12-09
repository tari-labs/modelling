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

def mva(_list):
    mva = []
    for i in range(len(_list)):
        if i < 50:
            mva.append(mean(_list[0:i+1]))
        else:
            mva.append(mean(_list[i-50:i+1]))
    return mva

noExp = int(input('Enter the number of experiments: '))
simTime = float(input('Enter simulation time(hours): '))
noAlgos = int(input('Enter the number of mining algorithms: '))

algos = []
for algo in range(0, noAlgos):
    algos.append([input('Assign name to algorithm %d: ' %(algo + 1))])
    
for algo in algos:
    algo.append(int(input('Enter initial hashrate of %s: ' % algo[0])))
    
for algo in algos:
    algo.append(int(input('Enter True target difficulty of %s: ' % algo[0])))
    
i_algo = int(input('Which algorithm do you want to alter hash rate for?[1-n]: ')) - 1

T_x = []
for i in range(1, 5):
    T_x.append(int(input('What is T%d hash power of %s: ' % (i, algos[i_algo][0]))))
    
seconds = int(simTime * 3600)
interval = int(seconds/5)

transposed = list(map(list, zip(*algos)))
_probs = probs(transposed[1], transposed[2])
transposed.append(_probs)
transposed.append([0] * len(transposed[0]))
_empty = []
for i in range(0, len(transposed[0])):
    _empty.append([])
_new = deepcopy(_empty)
_new2 = deepcopy(_empty)
transposed.append(_empty)
transposed.append(_new)
transposed.append(_new2)

_pr = 0.0166667 * 3
count = 0
check = interval
for j in range(0, seconds):
    if j > check:
        transposed[1][i_algo] = T_x.pop(0)
        check += interval
    if(random.uniform(0, 1) < _pr):
        count += 1
        _try = random.uniform(0, 1)
        cum = cumsum(transposed[3])
        for i in range(0, len(transposed[3])):
            if _try < cum[i]:
                transposed[5][i].append(transposed[4][i])
                transposed[6][i].append(transposed[2][i])
                transposed[7][i].append(j)
                transposed[4][i] = -1
                transposed[2][i] = adjustDifficulty(transposed[6][i], transposed[5][i], 60)
                transposed[3] = probs(transposed[1], transposed[2])
                break
    for k in range(0, len(transposed[4])):
        transposed[4][k] += 1
        
plt.figure(figsize=(15,10))
plt.xlabel('Time(s)')
plt.ylabel('Difficulty')
plt.title('Difficulty accross time')
for i in range(0, len(transposed[0])):
    plt.plot(transposed[7][i], (transposed[6][i]), label = transposed[0][i])
for i in range(1,5):
    plt.axvline(x = i * interval, color = 'red')
plt.legend(loc = 'best')
plt.show()

plt.figure(figsize=(15,10))
plt.xlabel('Time(s)')
plt.ylabel('Solve time')
plt.title('Solve time of algorithms')
for i in range(0, len(transposed[0])):
    plt.plot(transposed[7][i], mva(transposed[5][i]), label = transposed[0][i])
for i in range(1,5):
    plt.axvline(x = i * interval, color = 'red')
plt.legend(loc = 'best')
plt.show()
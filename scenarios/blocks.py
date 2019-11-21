import pandas as pd
from copy import deepcopy

def getDifficulty(diff, prevTime, time, difficultyAdjustment):
    try:
        if prevTime >= time:
            return diff + min((diff * (1 + time/prevTime)), difficultyAdjustment)
        else:
            return diff - min((diff * (1 - time/prevTime)), difficultyAdjustment)
    except:
        return 1

def getProbability(prevTime, time, prob = 0.3333):
    if prevTime >= time:
        return prob - ((prevTime - time) / time) * prob
    else:
        return prob + ((time - prevTime) / time) * prob

targetBlockTime = int(input('What is target block time?: '))
noOFBlocks = int(input('How many blocks are you considering?: '))
miningAlgos = int(input('Number of mining algorithms: '))

algos = []
hashPower = int(input('What is hash power of mining algorithm: '))
algos.append([hashPower])
for i in range(0, MiningAlgos - 1):
    message = 'What is hash power of independant %s? ' % str(i+1)
    hashPower = int(input(message))
    message = 'What will be the factor to increase hash power of Independent %s? ' % str(i+1)
    hashFactor = float(input(message))
    algos.append([hashPower, hashFactor])
    
difficulty = 300
difficultyAdjustment = 15
time = targetBlockTime * miningAlgos

blocks = []
blockRow = []
blockRow.append(algos[0][0])
blockRow.append(algos[0][0] * time)
blockRow.append(time)
blockRow.append(1/miningAlgos)
blockRow.append(algos[1][0])
blockRow.append(algos[1][0] * time)
blockRow.append(time)
blockRow.append(1/miningAlgos)
blockRow.append(algos[2][0])
blockRow.append(algos[1][0] * time)
blockRow.append(time)
blockRow.append(1/miningAlgos)
blocks.append(blockRow)
prev = deepcopy(blockRow)
for i in range(1, noOFBlocks):
    blockRow = []
    #for algo in algos:
        #if len(algo) == 1:
    blockRow.append(algos[0][0])
    blockRow.append(algos[0][0] * time)
    blockRow.append(time)
    blockRow.append(1/miningAlgos)

    blockRow.append(prev[4] + prev[4]* algos[1][1])
    blockRow.append(getDifficulty(prev[5], prev[6], time, difficultyAdjustment))
    blockRow.append(blockRow[4]/blockRow[5])
    blockRow.append(getProbability(blockRow[6], time))
    blockRow.append(prev[8] + prev[8]* algos[2][1])
    blockRow.append(getDifficulty(prev[9], prev[10], time, difficultyAdjustment))
    blockRow.append(blockRow[8]/blockRow[9])
    blockRow.append(1-(blockRow[3] + blockRow[7]))
    prev = blockRow
    blocks.append(blockRow)
    
df = pd.DataFrame.from_records(blocks)
df.columns = ['A: hash rate', 'A: Difficulty', 'A: Block time', 'A: P(A)', 'B: hash rate', 'B: Difficulty', 'B: Block time', 'A: P(B)', 'C: hash rate', 'C: Difficulty', 'C: Block time', 'C: P(C)']


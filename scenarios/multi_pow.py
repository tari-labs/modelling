from statistics import mean
import random
import matplotlib.pyplot as plt
import numpy as np
import heapq

def get_indexes_max_n_values(my_list, count):
    max_values = heapq.nlargest(count, my_list)
    max_values = list(set(max_values)) #Use unique values only
    indexes = []
    for i in range(0, len(max_values)):
        for j in range(0, len(my_list)):
            if max_values[i] == my_list[j]:
                indexes.append(j)
    return indexes

def limit_down(num, value):
    if num < value:
        return value
    else:
        return num

class COUNTER:
    def __init__(self, initial_value=0, increment=1):
        self.new = initial_value
        self.old = initial_value
        self.initial_value = initial_value
        self.increment = increment
        
    def reset(self):
        self.new = self.initial_value
        self.old = self.initial_value
        
    def incr(self):
        self.old = self.new
        self.new += self.increment
        return self.old

#Linear Weighted Moving Average - Basic
class DIFFICULTY_LWMA_00:
    def __init__(self, difficulty_window):
        self.difficulty_window = difficulty_window
    
    def adjust_difficulty(self, difficulties, solve_times, target_time):
        n = self.difficulty_window if len(difficulties) > self.difficulty_window else len(difficulties)
        avg_diff = mean(difficulties[len(difficulties)-n:])
        _sum = 0
        denom = 0
        n = self.difficulty_window if len(solve_times) > self.difficulty_window else len(solve_times)
        for i in range(len(solve_times)-n, len(solve_times)):
            _sum += (solve_times[i] * (i+1))
            denom += (i+1)
        return avg_diff * (target_time/(_sum/denom))


#Linear Weighted Moving Average - Bitcoin & Zcash Clones 
#(https://github.com/zawy12/difficulty-algorithms/issues/3)
class DIFFICULTY_LWMA_01:
    def __init__(self, difficulty_window):
        self.difficulty_window = difficulty_window
    
    def adjust_difficulty(self, difficulties, solve_times, target_time):
        N = self.difficulty_window if len(difficulties) > self.difficulty_window else len(difficulties)
        L = 0
        T = target_time
        for i in range(len(solve_times)-N, len(solve_times)):
            L += (i - len(solve_times)-N + 1) * min(6*T, solve_times[i])
        if L < N*N*T/20:
            L =  N*N*T/20
        if N > 1:
            avg_D = limit_down((difficulties[len(difficulties)-1] - difficulties[len(difficulties)-N] )/ N, difficulties[0])
            #avg_D = mean(difficulties[len(difficulties)-N:])
        else:
            avg_D = difficulties[0]
        if avg_D > 2000000*N*N*T:
            next_D = (avg_D/(200*L))*(N*(N+1)*T*99)
        else:
            next_D = (avg_D*N*(N+1)*T*99)/(200*L)
        print('N=', N, '  L=', L, '  avg_D=', avg_D, '  next_D=', next_D)
        return  next_D

#Block time based on ratio between target difficulty and available hash rate
class MINE_BLOCK:
    def __init__(self, randomness, noAlgos):
        randomness = min(abs(randomness), 0.9)
        self.rand_down = (1-randomness)
        self.rand_up = (1+randomness)
        self.noAlgos = noAlgos

    def calc_block_hash(self, difficulty, hash_rate, gradient, intercept):
        gradient_ = random.uniform(gradient*self.rand_down, gradient*self.rand_up)
        intercept_ = random.uniform(intercept*self.rand_down, intercept*self.rand_up)
        block_time = limit_down((difficulty/hash_rate) * gradient_ + intercept_, 1)
        achieved_difficulty = difficulty + abs(difficulty - ((block_time - intercept) / gradient) * hash_rate)
        return block_time, achieved_difficulty

class BLOCK:
    def __init__(self, block_number, algo, achieved_difficulty, accumulated_difficulty, block_time, hash_rate):
        self.block_number = int(block_number)
        self.algo = int(algo)
        self.achieved_difficulty = float(achieved_difficulty)
        self.accumulated_difficulty = float(accumulated_difficulty)
        self.block_time = float(block_time)
        self.hash_rate = hash_rate
        
#Blockchain
class BLOCKCHAIN:
    def __init__(self, selfish_mining, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates):
        self.selfish_mining = selfish_mining
        self.noAlgos = noAlgos
        self.chain = []
        self.target_difficulties = [[] for i in range(self.noAlgos)]
        self.achieved_difficulties = [[] for i in range(self.noAlgos)]
        self.accumulated_difficulties = [[] for i in range(self.noAlgos)]
        self.block_times = [[] for i in range(self.noAlgos)]
        self.hash_rates = [[] for i in range(self.noAlgos)]
        for i in range(self.noAlgos):
            self.target_difficulties[i].append(initial_difficulties[i])
            self.achieved_difficulties[i].append(initial_difficulties[i])
            self.accumulated_difficulties[i].append(initial_difficulties[i])
            self.block_times[i].append(initial_block_time)
            self.hash_rates[i].append(initial_hash_rates[i])

    def get_difficulties_per_algo(self):
        return self.difficulties

    def get_block_times_per_algo(self):
        return self.block_times

    def get_hash_rates_per_algo(self):
        return self.hash_rates

    def get_achieved_difficulties(self):
        achieved_difficulties = []
        for i in range(0, len(self.chain)):
            achieved_difficulties.append(self.chain[i].achieved_difficulty)
        return achieved_difficulties

    def get_accumulated_difficulties(self):
        accumulated_difficulties = []
        for i in range(0, len(self.chain)):
            accumulated_difficulties.append(self.chain[i].accumulated_difficulty)
        return accumulated_difficulties

    def get_block_times(self):
        block_times = []
        for i in range(0, len(self.chain)):
            block_times.append(self.chain[i].block_time)
        return block_times

    def get_hash_rates(self):
        hash_rates = []
        for i in range(0, len(self.chain)):
            hash_rates.append(self.chain[i].hash_rate)
        return hash_rates

    def get_algo(self):
        algo = []
        repeats = []
        counts = [1 for i in range(self.noAlgos)]
        for i in range(0, len(self.chain)):
            algo.append(self.chain[i].algo)
            #Count repeats
            if i>0:
                if (self.chain[i].algo == self.chain[i-1].algo) and (i < len(self.chain)-1):
                    counts[self.chain[i].algo] += 1
                else:
                    repeats.append([i-1, self.chain[i-1].algo, counts[self.chain[i-1].algo]])
                    counts[self.chain[i-1].algo] = 1
        repeats = list(map(list, zip(*repeats))) #data into row-column format
        return algo, repeats

    def add_block(self, block_times, target_difficulties, achieved_difficulties, hash_rates, init=False):
        debug = False
        #Determine accumulated difficulties (geometric mean) for all competing algorithms
        geometric_mean = [[] for i in range(self.noAlgos)]
        difficulties = [[] for i in range(self.noAlgos)]
        for i in range(0, self.noAlgos):
            #Add achieved difficulty to accmulated difficulty for current algo, else use previous accmulated difficulty
            for j in range(0, self.noAlgos):
                if i == j:
                    difficulties[j] = self.accumulated_difficulties[j][len(self.accumulated_difficulties[j])-1] + \
                        achieved_difficulties[j]
                else:
                    difficulties[j] = self.accumulated_difficulties[j][len(self.accumulated_difficulties[j])-1]
            #Debug ˅˅˅˅˅˅˅˅˅˅˅˅˅˅
            if init==False and debug==True:
                print(difficulties)
            #Debug ˄˄˄˄˄˄˄˄˄˄˄˄˄˄
            #Geometric mean for current algo
            geometric_mean[i] = 1
            for j in range(0, self.noAlgos):
                geometric_mean[i] *=  difficulties[j]
            geometric_mean[i] = pow(geometric_mean[i], 1/self.noAlgos)
        #Debug ˅˅˅˅˅˅˅˅˅˅˅˅˅˅
        if init==False and debug==True:
            print('')
            print(geometric_mean, ' ', geometric_mean.index(max(geometric_mean)))
            print('')
        #Debug ˄˄˄˄˄˄˄˄˄˄˄˄˄˄
        #Select algorithm with highest accumulated difficulty
        if init==True:
            algo = geometric_mean.index(max(geometric_mean)) # algo = len(self.chain) % self.noAlgos
        else:
            algo = geometric_mean.index(max(geometric_mean))
        #Add new block to the blockchain
        self.chain.append(BLOCK(len(self.chain), algo, achieved_difficulties[algo], geometric_mean[algo], \
                           block_times[algo], hash_rates[algo]))
        #Update blockchain stats
        self.target_difficulties[algo].append(target_difficulties[algo])
        self.achieved_difficulties[algo].append(achieved_difficulties[algo])
        accumulated_difficulty = self.accumulated_difficulties[algo][len(self.accumulated_difficulties[algo])-1] + \
                        achieved_difficulties[algo]
        self.accumulated_difficulties[algo].append(accumulated_difficulty)
        self.block_times[algo].append(block_times[algo])
        self.hash_rates[algo].append(hash_rates[algo])

    def reorg():
        return


#Constants
c = COUNTER(initial_value=0, increment=1)
_NAM = c.incr() #Name
_GRA = c.incr() #Gradient
_INT = c.incr() #Intercept
_HR0 = c.incr() #Initial hash rate
_DF0 = c.incr() #Initial difficulty
_BT0 = c.incr() #Initial block time

#Mining algorithm choices
algos = []
algos.append(['Algo 1', 119.12, 0.8809, 1000, 1])
algos.append(['Algo 2', 148.94, 0.8511, 10000, 10])
algos.append(['Algo 3', 198.66, 0.8013, 100000, 100])
algos.append(['Algo 4', 298.25, 0.7018, 1000000, 1000])
algos.append(['Algo 5', 597.99, 0.4020, 10000000, 10000])
algos = list(map(list, zip(*algos))) #data into row-column format


blocksToSolve =       int(input('Enter number of blocks to solve after initial period: '))
noAlgos =         min(int(input('Enter the number of mining algorithms (1-5):          ')), len(algos))
targetBT =            int(input('Enter the system target block time:                   '))
difficulty_window =   int(input('Enter the difficulty algo window:                     '))
mining_randomness = float(input('Enter the mining randomness factor (0-0.9):           '))

#Assign initial fixed data to algorithms
data = []
data.append(algos[_NAM][0:noAlgos]) #_NAM
data.append(algos[_GRA][0:noAlgos]) #_GRA
data.append(algos[_INT][0:noAlgos]) #_INT
data.append(algos[_HR0][0:noAlgos]) #_HR0
data.append(algos[_DF0][0:noAlgos]) #_DF0
data.append([targetBT for i in range(noAlgos)]) #_BT0

#Intialize data
diff_algo = DIFFICULTY_LWMA_00(difficulty_window=difficulty_window)
miner = MINE_BLOCK(randomness=mining_randomness, noAlgos=noAlgos)
chain = BLOCKCHAIN(selfish_mining=False, noAlgos=noAlgos, initial_difficulties=data[_DF0], initial_block_time=1, \
                   initial_hash_rates=data[_HR0])

#For debugging
diff_algo_vars = vars(diff_algo)
miner_vars = vars(miner)
chain_vars = vars(chain)

#Initial: Adjusting difficulty to achieve target block time
settling_window = int(abs(diff_algo.difficulty_window*1.5*noAlgos))
target_difficulties = [[] for i in range(noAlgos)]
block_times = [[] for i in range(noAlgos)]
achieved_difficulty = [[] for i in range(noAlgos)]
hash_rates = [[] for i in range(noAlgos)]
for i in range(1, settling_window): #0th elements are the initial values
    for j in range(0, noAlgos):
        #Difficulty adjustment
        target_difficulties[j] = diff_algo.adjust_difficulty(chain.achieved_difficulties[j], chain.block_times[j], data[_BT0][j])
        #Available hash rate
        hash_rates[j] = chain.hash_rates[j][len(chain.hash_rates[j])-1] #Hash rate stays constant during initial phase
        #Mine block
        block_times[j], achieved_difficulty[j] = miner.calc_block_hash(target_difficulties[j], hash_rates[j], data[_GRA][j], data[_INT][j])
    #Derermine and add winning block to the blockchain
    chain.add_block(block_times, target_difficulties, achieved_difficulty, hash_rates, init=True)

#Scenario starts here
for i in range(settling_window, settling_window+blocksToSolve): #0th elements are the initial values
    for j in range(0, noAlgos):
        #Difficulty adjustment
        target_difficulties[j] = diff_algo.adjust_difficulty(chain.achieved_difficulties[j], chain.block_times[j], data[_BT0][j])
        #Game theory adjusting hash rate
        if i > settling_window + blocksToSolve/(noAlgos*2) and i < settling_window + blocksToSolve/(noAlgos) and j == 0:
            hash_rates[j] = chain.hash_rates[j][0]*2
        else:
            hash_rates[j] = chain.hash_rates[j][0] #Hash rate stays constant during initial phase
        #Mine block
        block_times[j], achieved_difficulty[j] = miner.calc_block_hash(target_difficulties[j], hash_rates[j], data[_GRA][j], data[_INT][j])
    #Derermine and add winning block to the blockchain
    chain.add_block(block_times, target_difficulties, achieved_difficulty, hash_rates)

       
#Plot results
fig1, axs1 = plt.subplots(noAlgos, 3, figsize=(15, noAlgos*5))
fig1.subplots_adjust(hspace=0.3, wspace=0.3)
for i in range(0, noAlgos):
    if noAlgos < 2:
        x = np.arange(1, len(chain.hash_rates[i]) + 1)
        axs1[0].plot(x, chain.hash_rates[i])
        axs1[0].set_title(data[_NAM][i] + ': Hash rate')
        axs1[0].grid()
        x = np.arange(1, len(chain.target_difficulties[i]) + 1)
        axs1[1].plot(x, chain.target_difficulties[i], x, chain.achieved_difficulties[i])
        axs1[1].set_title(data[_NAM][i] + ': Difficulty')
        axs1[1].grid()
        x = np.arange(1, len(chain.block_times[i]) + 1)
        axs1[2].plot(x, chain.block_times[i])
        axs1[2].set_title(data[_NAM][i] + ': Solve time')
        axs1[2].grid()
    else:
        x = np.arange(1, len(chain.hash_rates[i]) + 1)
        axs1[i, 0].plot(x, chain.hash_rates[i])
        axs1[i, 0].set_title(data[_NAM][i] + ': Hash rate')
        axs1[i, 0].grid()
        x = np.arange(1, len(chain.target_difficulties[i]) + 1)
        axs1[i, 1].plot(x, chain.target_difficulties[i], x, chain.achieved_difficulties[i])
        axs1[i, 1].set_title(data[_NAM][i] + ': Difficulty')
        axs1[i, 1].grid()
        x = np.arange(1, len(chain.block_times[i]) + 1)
        axs1[i, 2].plot(x, chain.block_times[i])
        axs1[i, 2].set_title(data[_NAM][i] + ': Solve time')
        axs1[i, 2].grid()

plt.show()

fig2, axs2 = plt.subplots(2, 2, figsize=(15, 10))

y = chain.get_block_times()
x = np.arange(1, len(y) + 1)
axs2[0, 0].plot(x, y)
axs2[0, 0].set_title('Blockchain: Block times')
axs2[0, 0].grid()

y = chain.get_accumulated_difficulties()
x = np.arange(1, len(y) + 1)
axs2[0, 1].plot(x, y)
axs2[0, 1].set_title('Blockchain: Accumulated difficulty')
axs2[0, 1].grid()

y, repeats = chain.get_algo()
x = np.arange(1, len(y) + 1)
axs2[1, 0].plot(x, y, marker='*', ls='')
axs2[1, 0].set_title('Blockchain: Algo')
axs2[1, 0].grid()
   
axs2[1, 1].plot(repeats[0], repeats[2], marker='*', ls='')
axs2[1, 1].set_title('Blockchain: Repeats')
axs2[1, 1].grid()
y_max = get_indexes_max_n_values(repeats[2], count=5)
for i in range(0, len(y_max)):
    axs2[1, 1].text(repeats[0][y_max[i]] - repeats[0][len(repeats[0])-1]/20, \
        repeats[2][y_max[i]] - max(repeats[2])/15, \
        r'(' + str(data[0][repeats[1][y_max[i]]]) + ')')
 
plt.show()

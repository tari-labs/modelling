import matplotlib.pyplot as plt
import numpy as np
import heapq
import os
import copy

#%% Functions header
#------------------------------------
#----------- Functions --------------
#------------------------------------

#%% Get indexes for n maximum values
def get_indexes_max_n_values(my_list, count):
    max_values = heapq.nlargest(count, my_list)
    max_values = list(set(max_values)) #Use unique values only
    indexes = []
    for i in range(0, len(max_values)):
        for j in range(0, len(my_list)):
            if max_values[i] == my_list[j]:
                indexes.append(j)
    return indexes

#%% Limit number down to minimum value
def limit_down(num, min_value):
    return max(num, min_value)

#%% Limit number to between minimum and maximum values
def limit_up_down(num, min_value, max_value):
    return (min(max(num, min_value), max_value))

#%% Input helper - returns default (typed) value upon no input
def get_input(my_text, default, my_type=None):
    if default != '':
        my_text = my_text + '[' + str(default) + ']: '
    else:
        my_text = my_text + '[?]: '
    the_input = input(my_text)
    if the_input == '' and default != None:
        the_input = default
    if my_type == 'int':
        the_input = int(the_input)
    elif my_type == 'float':
        the_input = float(the_input)
    else:
        the_input = str(the_input)
    return the_input

#%% Classes header
#------------------------------------
#----------- Classes ----------------
#------------------------------------

#%% Simple counter
class COUNTER:
    def __init__(self, initial_value=0, increment=1):
        self.new = initial_value
        self.old = initial_value
        self.initial_value = initial_value
        self.increment = increment

    def reset(self, initial_value=0):
        self.new = initial_value
        self.old = initial_value

    def incr(self):
        self.old = self.new
        self.new += self.increment
        return self.old

    def val(self):
        return self.old

#%% Linear Weighted Moving Average - Basic
class DIFFICULTY_LWMA_00:
    def __init__(self, difficulty_window):
        self.difficulty_window = difficulty_window

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time):
        n = self.difficulty_window if len(solve_times) > self.difficulty_window else len(solve_times)
        avg_diff = np.mean(difficulties[len(difficulties)-n:])
        _sum = 0
        denom = 0
        for i in range(len(solve_times)-n, len(solve_times)):
            _sum += (solve_times[i] * (i+1))
            denom += (i+1)
        return avg_diff * (target_time/(_sum/denom))

#%% #Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2017-12-06
#(https://github.com/zawy12/difficulty-algorithms/issues/3#issue-279773112)
class DIFFICULTY_LWMA_01_20171206:
    def __init__(self, difficulty_window):
        self.difficulty_window = difficulty_window

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time):
        N = self.difficulty_window if len(solve_times) > self.difficulty_window else len(solve_times)
        L = 0
        T = target_time
        for i in range(1, N+1):
            j = len(solve_times)-N + (i - 1) #only the last portion of the list must be indexed
            L += i * min(6*T, solve_times[j])
        if L < N*N*T/20:
            L =  N*N*T/20
        if N > 1:
            avg_D = limit_down((acc_difficulties[len(acc_difficulties)-1] - acc_difficulties[len(acc_difficulties)-N]) / N, \
                               acc_difficulties[0])
        else:
            avg_D = acc_difficulties[0]
        next_D = (avg_D/(200*L))*(N*(N+1)*T*99) #The original algo uses an if statement here that resolves to the same answer
        return  next_D

#%% #Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2018-11-27
#(https://github.com/zawy12/difficulty-algorithms/issues/3#issuecomment-442129791)
#(https://github.com/tari-project/tari/blob/development/base_layer/core/src/proof_of_work/lwma_diff.rs)
class DIFFICULTY_LWMA_01_20181127:
    def __init__(self, difficulty_window):
        self.difficulty_window = difficulty_window

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time):
        n = self.difficulty_window if len(solve_times) > self.difficulty_window else len(solve_times)
        k = np.int64(n * (n + 1) * target_time / 2)
        weighted_times = np.int64(0)
        j = np.int64(0)
        for i in range(len(solve_times)-n, len(solve_times)):
            solve_time = np.int64(min(6*target_time, solve_times[i]))
            j += 1
            weighted_times += solve_time * j
        if n > 1:
            ave_difficulty = limit_down((acc_difficulties[len(acc_difficulties)-1] -
                                         acc_difficulties[len(acc_difficulties)-n]) / n, acc_difficulties[0])
        else:
            ave_difficulty = acc_difficulties[0]
        target = ave_difficulty * k / weighted_times
        return  target

#%% Block time based on ratio between target difficulty and available hash rate
class MINE_BLOCK:
    def __init__(self, randomness_miner, randomness_hash_rate, noAlgos, initial_hash_rates, dist):
        self.randomness_miner = limit_up_down(randomness_miner, 0, 0.9)
        self.rand_down_m = (1-self.randomness_miner)
        self.rand_up_m = (1+self.randomness_miner)
        self.randomness_hash_rate = limit_up_down(randomness_hash_rate, 0, 0.9)
        self.rand_down_hr = (1-self.randomness_hash_rate)
        self.rand_up_hr = (1+self.randomness_hash_rate)
        self.noAlgos = noAlgos
        self.initial_hash_rates = initial_hash_rates
        if self.randomness_miner > 0 or self.randomness_hash_rate > 0:
            if dist == 'normal': #'uniform' or 'normal' or 'poisson'
                self.dist = 'normal'
                print(' ----- Randomness => normal distribution -----\n')
            elif dist == 'poisson':
                self.dist = 'poisson'
                print(' ----- Randomness => poisson distribution -----\n')
            elif dist == 'uniform':
                self.dist = 'uniform'
                print(' ----- Randomness => uniform distribution -----\n')
            else:
                self.dist = ''
                print(' ----- Randomness => none -----\n')
        else:
            self.dist = ''
            print(' ----- Randomness => none -----\n')
        self.count = COUNTER(initial_value=0, increment=1)

    def get_hash_rate(self, hash_rate, algo):
        if self.randomness_hash_rate > 0:
            min_value = self.initial_hash_rates[algo]/10
            if self.dist == 'normal':
                hash_rate = limit_down(np.random.normal(hash_rate, hash_rate*self.randomness_hash_rate, 1), min_value)
            elif self.dist == 'poisson':
                hash_rate = limit_down(np.random.poisson(hash_rate, 1), min_value)
            elif self.dist == 'uniform':
                hash_rate = limit_down(np.random.uniform(hash_rate*self.rand_down_hr, hash_rate*self.rand_up_hr), min_value)
        return hash_rate

    def calc_block_hash(self, difficulty, hash_rate, gradient, intercept):
        self.count.reset()
        while self.count.incr() <= 10:
            if self.randomness_miner > 0:
                if self.dist == 'normal':
                    gradient_r = np.random.normal(gradient*self.rand_down_m, gradient*self.randomness_miner, 1)
                    intercept_r = np.random.normal(intercept*self.rand_down_m, intercept*self.randomness_miner, 1)
                elif self.dist == 'poisson':
                    gradient_r = np.random.poisson(gradient, 1)
                    intercept_r = np.random.poisson(intercept, 1)
                elif self.dist == 'uniform':
                    gradient_r = np.random.uniform(gradient*self.rand_down_m, gradient)
                    intercept_r = np.random.uniform(intercept*self.rand_down_m, intercept)
                else:
                    gradient_r = gradient
                    intercept_r = intercept
            else:
                gradient_r = gradient
                intercept_r = intercept
            block_time = limit_down((difficulty/hash_rate) * gradient_r + intercept_r, 1)
            achieved_difficulty = difficulty + (difficulty - ((block_time - intercept) / gradient) * hash_rate) #abs(difficulty - ((block_time - intercept) / gradient) * hash_rate)
            if achieved_difficulty >= difficulty:
                break
        else:
            achieved_difficulty = difficulty
            block_time = limit_down((difficulty/hash_rate) * gradient + intercept, 1)
        return block_time, achieved_difficulty

#%% Basic block
class BLOCK:
    def __init__(self, block_number, algo, achieved_difficulty, accumulated_difficulty, block_time, hash_rate):
        self.block_number = int(block_number)
        self.algo = int(algo)
        self.achieved_difficulty = float(achieved_difficulty)
        self.accumulated_difficulty = float(accumulated_difficulty)
        self.block_time = float(block_time)
        self.hash_rate = hash_rate

#%% Blockchain
class BLOCKCHAIN:
    def __init__(self, selfish_mining, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates, \
                 reorg_ignore_factor, use_geometric_mean):
        self.selfish_mining = selfish_mining
        self.noAlgos = noAlgos
        self.chain = []
        self.target_difficulties = [[] for i in range(self.noAlgos)]
        self.achieved_difficulties = [[] for i in range(self.noAlgos)]
        self.accumulated_difficulties = [[] for i in range(self.noAlgos)]
        self.block_times = [[] for i in range(self.noAlgos)]
        self.hash_rates = [[] for i in range(self.noAlgos)]
        self.use_geometric_mean = use_geometric_mean
        self.reorg_ignore_factor = reorg_ignore_factor
        for i in range(self.noAlgos):
            self.target_difficulties[i].append(initial_difficulties[i])
            self.achieved_difficulties[i].append(initial_difficulties[i])
            self.accumulated_difficulties[i].append(initial_difficulties[i])
            self.block_times[i].append(initial_block_time)
            self.hash_rates[i].append(initial_hash_rates[i])

    def get_achieved_difficulties_per_algo(self):
        return self.achieved_difficulties

    def get_accumulated_difficulties_per_algo(self):
        return self.accumulated_difficulties

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
            #Geometric mean (overflow resistant) for current algo
            geometric_mean[i] = 0
            for j in range(0, self.noAlgos):
                geometric_mean[i] +=  np.log(difficulties[j])
            geometric_mean[i] = np.exp(geometric_mean[i]/self.noAlgos)
        #Debug ˅˅˅˅˅˅˅˅˅˅˅˅˅˅
        if init==False and debug==True:
            print('')
            print(geometric_mean, ' ', geometric_mean.index(max(geometric_mean)))
            print('')
        #Debug ˄˄˄˄˄˄˄˄˄˄˄˄˄˄
        #Select algorithm with highest accumulated difficulty limted by difference in solve times
        # - This can be used to initialize the difficulty algorithms during init to choose alternate algos
        #     algo = len(self.chain) % self.noAlgos
        if self.use_geometric_mean == True:
            gm = [[i for i in range(0, len(geometric_mean))], copy.deepcopy(geometric_mean)]
            bt = copy.deepcopy(block_times)
            while max(bt) > self.reorg_ignore_factor * min(bt):
                t1 = bt.index(max(bt))
                bt.pop(t1)
                gm[0].pop(t1)
                gm[1].pop(t1)
            if len(block_times) == len(bt):
                algo = geometric_mean.index(max(geometric_mean))
            else:
                algo = gm[0][gm[1].index(max(gm[1]))]
                #print(block_times, bt, geometric_mean.index(max(geometric_mean)), 'vs', algo, '  at ', len(self.chain))
        else:
            algo = block_times.index(min(block_times))
        #Add new block to the blockchain
        self.chain.append(BLOCK(len(self.chain), algo, achieved_difficulties[algo], geometric_mean[algo], \
                           block_times[algo]/self.noAlgos, hash_rates[algo]))
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

#%% Main program header
#------------------------------------
#----------- Main Program -----------
#------------------------------------

#%% Algo constants
#Constants
c = COUNTER(initial_value=0, increment=1)
_NAM = c.incr() #Name
_GRA = c.incr() #Gradient
_INT = c.incr() #Intercept
_HR0 = c.incr() #Initial hash rate
_DF0 = c.incr() #Initial difficulty
_BT0 = c.incr() #Initial block time

#Mining algorithm choices (as per '../other/multi_pow_algos_approximation.*')
algos = []
algos.append(['Algo 1', 119.12, 0.8809, 1000, 1])
algos.append(['Algo 2', 148.94, 0.8511, 10000, 10])
algos.append(['Algo 3', 198.66, 0.8013, 100000, 100])
algos.append(['Algo 4', 298.25, 0.7018, 1000000, 1000])
algos.append(['Algo 5', 597.99, 0.4020, 10000000, 10000])
algos = list(map(list, zip(*algos))) #data into row-column format

#%% User inputs
#Read inputs from config file
blocksToSolve = noAlgos = diff_algo = targetBT = difficulty_window = mining_randomness = hash_rate_randomness = ignore_factor = ''
config_file = os.getcwd() + os.path.sep + "my_inputs.txt"
config_file_start_id = ">>>> Gtd$K46U%JN*X#Vd >>>>"
config_file_end_id = "<<<< Gtd$K46U%JN*X#Vd <<<<"
if os.path.isfile(config_file):
    with open(config_file,"r") as f:
        fl = f.readlines()
        c.reset()
        if fl[c.incr()].strip() == config_file_start_id.strip() and fl[len(fl)-1].strip() == config_file_end_id.strip():
            blocksToSolve = int(fl[c.incr()].strip())
            noAlgos = int(fl[c.incr()].strip())
            diff_algo = int(fl[c.incr()].strip())
            targetBT = int(fl[c.incr()].strip())
            difficulty_window = int(fl[c.incr()].strip())
            mining_randomness = float(fl[c.incr()].strip())
            hash_rate_randomness = float(fl[c.incr()].strip())
            reorg_ignore_factor = float(fl[c.incr()].strip())

#Get new iputs
blocksToSolve =           limit_down(get_input('Enter number of blocks to solve after initial period   ', default=blocksToSolve, my_type='int'), 0)
noAlgos =              limit_up_down(get_input('Enter the number of mining algorithms (1-%s)            ' % (len(algos)), default=noAlgos, my_type='int'), 1, len(algos))
diff_algo =            limit_up_down(get_input('Diff algo: LWMA(0), LWMA-1_171206(1), LWMA-1_181127(2) ', default=diff_algo, my_type='int',), 0, 2)
targetBT =                limit_down(get_input('Enter the system target block time (>=10)              ', default=targetBT, my_type='int'), 10)
difficulty_window =       limit_down(get_input('Enter the difficulty algo window (>=1)                 ', default=difficulty_window, my_type='int',), 1)
mining_randomness =    limit_up_down(get_input('Enter the mining randomness factor (0-0.9)             ', default=mining_randomness, my_type='float',), 0, 0.9)
hash_rate_randomness = limit_up_down(get_input('Enter the hash rate randomness factor (0-0.9)          ', default=hash_rate_randomness, my_type='float',), 0, 0.9)
reorg_ignore_factor =  limit_up_down(get_input('Enter the reorg ignore factor (1.05-3)                 ', default=reorg_ignore_factor, my_type='float',), 1.05, 3)

#Write new inputs to config file
with open(config_file,"w+") as f:
    f.write(config_file_start_id + "\n")
    f.write(str(blocksToSolve) + "\n")
    f.write(str(noAlgos) + "\n")
    f.write(str(diff_algo) + "\n")
    f.write(str(targetBT) + "\n")
    f.write(str(difficulty_window) + "\n")
    f.write(str(mining_randomness) + "\n")
    f.write(str(hash_rate_randomness) + "\n")
    f.write(str(reorg_ignore_factor) + "\n")
    f.write(config_file_end_id)

#%% Initialize
#Assign initial fixed data to algorithms
data = []
data.append(algos[_NAM][0:noAlgos]) #_NAM
data.append(algos[_GRA][0:noAlgos]) #_GRA
data.append(algos[_INT][0:noAlgos]) #_INT
data.append(algos[_HR0][0:noAlgos]) #_HR0
data.append(algos[_DF0][0:noAlgos]) #_DF0
data.append([targetBT*noAlgos for i in range(noAlgos)]) #_BT0

#Intialize data
c.reset()
if diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window=difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA Basic -----\n')
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20171206(difficulty_window=difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA-1 version 2017-12-06 -----\n')
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20181127(difficulty_window=difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA-1 version 2018-11-27 -----\n')
else:
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window=difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA Basic -----\n')
miner = MINE_BLOCK(randomness_miner=mining_randomness, randomness_hash_rate=hash_rate_randomness, noAlgos=noAlgos, \
                   initial_hash_rates=data[_HR0], dist='poisson')
chain = BLOCKCHAIN(selfish_mining=False, noAlgos=noAlgos, initial_difficulties=data[_DF0], initial_block_time=1, \
                   initial_hash_rates=data[_HR0], reorg_ignore_factor=reorg_ignore_factor, use_geometric_mean=True)

#For debugging
diff_algo_vars = vars(diff_algo)
miner_vars = vars(miner)
chain_vars = vars(chain)

#%% Blockchain runtime
#Initial: Adjusting difficulty to achieve target block time
settling_window = int(abs(diff_algo.difficulty_window*1.5*noAlgos))
target_difficulties = [[] for i in range(noAlgos)]
block_times = [[] for i in range(noAlgos)]
achieved_difficulty = [[] for i in range(noAlgos)]
hash_rates = [[] for i in range(noAlgos)]
for i in range(1, settling_window): #0th elements are the initial values
    for j in range(0, noAlgos):
        #Difficulty adjustment
        target_difficulties[j] = diff_algo.adjust_difficulty(chain.achieved_difficulties[j], chain.accumulated_difficulties[j], \
                                                             chain.block_times[j], data[_BT0][j])
        #Available hash rate
        hash_rates[j] = miner.get_hash_rate(chain.hash_rates[j][0], j) #Hash rate stays constant during initial phase
        #Mine block
        block_times[j], achieved_difficulty[j] = miner.calc_block_hash(target_difficulties[j], hash_rates[j], data[_GRA][j], \
                                                                       data[_INT][j])
    #Determine and add winning block to the blockchain
    chain.add_block(block_times, target_difficulties, achieved_difficulty, hash_rates, init=True)

#Scenario starts here
for i in range(settling_window, settling_window+blocksToSolve): #0th elements are the initial values
    for j in range(0, noAlgos):
        #Difficulty adjustment
        target_difficulties[j] = diff_algo.adjust_difficulty(chain.achieved_difficulties[j], chain.accumulated_difficulties[j], \
                                                             chain.block_times[j], data[_BT0][j])
        #Game theory adjusting hash rate
        if i > settling_window + blocksToSolve/(noAlgos*2) and i < settling_window + blocksToSolve/(noAlgos) and j == 0:
            hash_rates[j] = miner.get_hash_rate(chain.hash_rates[j][0]*2, j)
        else:
            hash_rates[j] = miner.get_hash_rate(chain.hash_rates[j][0], j) #Hash rate stays constant during initial phase
        #Mine block
        block_times[j], achieved_difficulty[j] = miner.calc_block_hash(target_difficulties[j], hash_rates[j], data[_GRA][j], \
                                                                       data[_INT][j])
    #Derermine and add winning block to the blockchain
    chain.add_block(block_times, target_difficulties, achieved_difficulty, hash_rates)

#%% Plot results
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
axs2[1, 0].plot(x, y, marker='.', ls='')
axs2[1, 0].set_title('Blockchain: Algo')
axs2[1, 0].grid()

axs2[1, 1].plot(repeats[0], repeats[2], marker='.', ls='')
axs2[1, 1].set_title('Blockchain: Repeats')
axs2[1, 1].grid()
y_max = get_indexes_max_n_values(repeats[2], count=5)
for i in range(0, len(y_max)):
    axs2[1, 1].text(repeats[0][y_max[i]] - repeats[0][len(repeats[0])-1]/20, \
        repeats[2][y_max[i]] - max(repeats[2])/15, \
        r'(' + str(data[0][repeats[1][y_max[i]]]) + ')')

plt.show()

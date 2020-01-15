import matplotlib.pyplot as plt
import numpy as np
import heapq
import os
import copy

#%% Functions header
#------------------------------------
#----------- Functions --------------
#------------------------------------

#%% get_indexes_max_n_values
# Get indexes for n maximum values
def get_indexes_max_n_values(my_list, count):
    max_values = heapq.nlargest(count, my_list)
    max_values = list(set(max_values)) #Use unique values only
    indexes = []
    for i in range(0, len(max_values)):
        for j in range(0, len(my_list)):
            if max_values[i] == my_list[j]:
                indexes.append(j)
    return indexes

#%% limit_down
# Limit number down to minimum value
def limit_down(num, min_value):
    return max(num, min_value)

#%% limit_up
# Limit number up to maximum value
def limit_up(num, max_value):
    return min(num, max_value)

#%% limit_up_down
# Limit number to between minimum and maximum values
def limit_up_down(num, min_value, max_value):
    return (min(max(num, min_value), max_value))

#%% get_input
# Input helper - returns default (typed) value upon no input
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

#%% calc_geometric_mean
# Geometric mean (overflow resistant)
def calc_geometric_mean(n, previous_values, new_values):
    geometric_mean = [[] for i in range(n)]
    values = [[] for i in range(n)]
    for i in range(0, n):
        #Add new value to previous value for current member, else use previous value
        for j in range(0, n):
            if i == j:
                values[j] = previous_values[j] + new_values[j]
            else:
                values[j] = previous_values[j]
        geometric_mean[i] = 0
        for j in range(0, n):
            geometric_mean[i] +=  np.log(values[j])
        geometric_mean[i] = np.exp(geometric_mean[i]/n)
    return geometric_mean


#%% Classes header
#------------------------------------
#----------- Classes ----------------
#------------------------------------

#%% Class: COUNTER
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

#%% Class: DIFFICULTY_LWMA_00
#Linear Weighted Moving Average - Basic
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

#%% Class: DIFFICULTY_LWMA_01_20171206
#Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2017-12-06
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
            avg_D = limit_down((acc_difficulties[-1] - acc_difficulties[len(acc_difficulties)-N]) / N, \
                               acc_difficulties[0])
        else:
            avg_D = acc_difficulties[0]
        next_D = (avg_D/(200*L))*(N*(N+1)*T*99) #The original algo uses an if statement here that resolves to the same answer
        return  next_D

#%% Class: DIFFICULTY_LWMA_01_20181127
#Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2018-11-27
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
            ave_difficulty = limit_down((acc_difficulties[-1] -
                                         acc_difficulties[len(acc_difficulties)-n]) / n, acc_difficulties[0])
        else:
            ave_difficulty = acc_difficulties[0]
        target = ave_difficulty * k / weighted_times
        return  target

#%% Class: RANDOM_FUNC
class RANDOM_FUNC:
    def __init__(self, randomness, distribution, name, owner):
        self.randomness = limit_up_down(randomness, 0, 0.9)
        self.rand_down = (1 - self.randomness)
        self.rand_up = (1 + self.randomness)
        if self.randomness > 0:
            if str(distribution) == 'normal': #'uniform' or 'normal' or 'poisson'
                self.distribution = 'normal'
                print(' ----- %s: Randomness %s => normal distribution -----\n' % (name, owner))
            elif str(distribution) == 'poisson':
                self.distribution = 'poisson'
                print(' ----- %s: Randomness %s => poisson distribution -----\n' % (name, owner))
            elif str(distribution) == 'uniform':
                self.distribution = 'uniform'
                print(' ----- %s: Randomness %s => uniform distribution -----\n' % (name, owner))
            else:
                self.distribution = 'none'
                print(' ----- %s: Randomness %s => none -----\n' % (name, owner))
        else:
            self.distribution = 'none'
            print(' ----- %s: Randomness %s => none -----\n' % (name, owner))

    def get_value(self, value):
        if self.distribution == 'normal':
            value = np.random.normal(value*self.rand_down, value*self.randomness, 1)
        elif self.distribution == 'poisson':
            value = np.random.poisson(value, 1)
        elif self.distribution == 'uniform':
            value = np.random.uniform(value*self.rand_down, value)
        return value


#%% Class: HASH_RATE
class HASH_RATE:
    def __init__(self, initial_hash_rate, profile, randomness, dist, name):
        # 'initial_hash_rate': initial hash rate assigned to algo, also the default hash rate
        # 'profile'          : [ [[start_block_mumber_1, end_block_number_1], [start_ratio_1, end_ratio_1]], \
        #                        [[start_block_mumber_2, end_block_number_2], [start_ratio_2, end_ratio_2]] ]
        #                      ratio is a factor of the initial hash rate
        #                      block count starts after init phase ends
        # 'randomness'       : randomness factor with which the given hash rate can change
        # 'dist              : randomness distribution type
        self.rand = RANDOM_FUNC(randomness, dist, name, 'hash_rate')
        self.initial_hash_rate = abs(initial_hash_rate) #Only positive values
        self.min_randomness = 1
        self.profile = copy.deepcopy(profile)
        self.values = [self.initial_hash_rate for i in range(0, self.profile[-1][0][1]+1)]
        self.init = True
        self.n = 0
        #Hash rate from profile
        for i in range(0, len(self.profile)):
            for j in range(self.profile[i][0][0], self.profile[i][0][1]):
                delta = (self.profile[i][1][1] - self.profile[i][1][0]) / (self.profile[i][0][1] - self.profile[i][0][0])
                self.values[j] = self.initial_hash_rate * self.profile[i][1][0] + \
                    self.initial_hash_rate * (j - self.profile[i][0][0] + 1) * delta
        self.values[-1] = self.initial_hash_rate * self.profile[-1][1][1]

    def get_hash_rate(self, block_number, init):
        #Transition from init to not init
        if init == False and self.init == True:
            self.init = False
            self.n = block_number
        #Init phase
        if self.init == True:
            return self.initial_hash_rate
        #Run phase
        else:
            n = block_number - self.n
            #Get hash rate + bounds check
            if len(self.values) - 1 > n:
                hash_rate = self.values[n]
            else:
                hash_rate = self.values[-1]
            #Apply randomess
            hash_rate = self.rand.get_value(hash_rate)
            #Return
            return hash_rate

#%% Class: MINE_STRATEGY
class MINE_STRATEGY:
    def __init__(self, name):
        self.name = name

#%% Class: MINER
class MINER:
    def __init__(self, randomness_miner, dist, initial_difficulty, initial_block_time, \
                 gradient, intercept, name, algo_no, diff_algo, target_time, state):
        self.rand = RANDOM_FUNC(randomness_miner, dist, name, 'miner') #Object
        self.gradient = gradient
        self.intercept = intercept
        self.name = name
        self.algo_no = algo_no
        self.diff_algo = diff_algo #Object
        self.target_time = target_time
        self.count = COUNTER(initial_value=0, increment=1) #Object
        self.hash_rate = hash_rate #Object
        self.block_hash = BLOCK_HASH() #Object (singleton)
        self.blocks = []
        self.state = state
        #Own stats
        self.target_difficulties = []
        self.target_difficulties.append(initial_difficulty)
        self.achieved_difficulties = []
        self.achieved_difficulties.append(initial_difficulty)
        self.accumulated_difficulties = []
        self.accumulated_difficulties.append(initial_difficulty)
        self.block_times = []
        self.block_times.append(initial_block_time)
        self.hash_rates = []
        self.hash_rates.append(hash_rate.initial_hash_rate)

    #Block time based on ratio between target difficulty and available hash rate
    def solve_block(self, difficulty, block_number, init):
        self.count.reset()
        hash_rate = self.hash_rate.get_hash_rate(block_number, init)
        while self.count.incr() <= 10:
            gradient_r = self.rand.get_value(self.gradient)
            intercept_r = self.rand.get_value(self.intercept)
            block_time = limit_down((difficulty/hash_rate) * gradient_r + intercept_r, 1)
            achieved_difficulty = difficulty + (difficulty - ((block_time - self.intercept) / self.gradient) * hash_rate)
            if achieved_difficulty >= difficulty:
                break
        else:
            achieved_difficulty = difficulty
            block_time = limit_down((difficulty/hash_rate) * self.gradient + self.intercept, 1)
        return block_time, achieved_difficulty, hash_rate

    def create_block(self, difficulty, accumulated_difficulty, previous_hash, block_number, init):
        solve_time, achieved_difficulty, hash_rate = self.solve_block(difficulty, block_number, init)
        block_hash = self.block_hash.get_next_hash()
        accumulated_difficulty_ = accumulated_difficulty + achieved_difficulty
        block = BLOCK(block_number, block_hash, previous_hash, self.name, achieved_difficulty, accumulated_difficulty_, hash_rate, \
                 solve_time)
        return block

    def update_state(self, state, block_number, init):
        #ToDo strategy
        return

    def produce_next_blocks(self, block_number, init):
        target_difficulty = self.diff_algo.adjust_difficulty(self.state.achieved_difficulties[self.algo_no],
                                                             self.state.accumulated_difficulties[self.algo_no], \
                                                             self.state.block_times[self.algo_no], self.target_time)
        previous_hash = self.state.chain[-1].previous_hash
        #self.strategy.selfish_mining ToDo
        self.blocks.clear()
        self.blocks.append(self.create_block(target_difficulty, chain.accumulated_difficulties[self.algo_no], previous_hash, \
                                        block_number, init))
        return self.blocks


#%% Class: BLOCK_HASH_SHARED_STATE
#Shared state for the singleton block hash counter
class BLOCK_HASH_BORG:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

#%% Class: BLOCK_HASH
#Singleton block hash counter
class BLOCK_HASH(BLOCK_HASH_BORG):
    __instance = None
    def __init__(self):
        BLOCK_HASH_BORG.__init__(self)
        if BLOCK_HASH.__instance == None:
            BLOCK_HASH.__instance = True
            self.value = np.uint64(0)

    def get_next_hash(self):
        self.value += np.uint64(1)
        return self.value

    def reset(self):
        BLOCK_HASH.__instance = None
        BLOCK_HASH()
        return

#%% Class: BLOCK
class BLOCK:
    def __init__(self, block_number, block_hash, previous_hash, algo, achieved_difficulty, accumulated_difficulty, hash_rate, \
                 solve_time):
        self.algo = int(algo)
        self.achieved_difficulty = float(achieved_difficulty)
        self.accumulated_difficulty = float(accumulated_difficulty)
        self.solve_time = float(solve_time)
        self.hash_rate = float(hash_rate)
        self.block_number = np.uint64(block_number)
        self.block_hash = np.uint64(block_hash)
        self.previous_hash = np.uint64(previous_hash)

    def finalize(self, block_time, time_stamp, geometric_mean):
        self.block_time = float(block_time)
        self.time_stamp = float(time_stamp)
        self.geometric_mean = float(geometric_mean)

#%% Class: BLOCKCHAIN_SHARED_STATE
#Shared state for the singleton blockchain
class BLOCKCHAIN_STATE_BORG:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

#%% Class: BLOCKCHAIN_STATE
class BLOCKCHAIN_STATE(BLOCKCHAIN_STATE_BORG):
    __instance = None
    def __init__(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates):
        #Initialize singleton
        BLOCKCHAIN_STATE_BORG.__init__(self)
        #Other
        if BLOCKCHAIN_STATE.__instance == None:
            BLOCKCHAIN_STATE.__instance = True
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

    def reset(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates):
        BLOCKCHAIN_STATE.__instance = None
        BLOCKCHAIN_STATE(noAlgos, initial_difficulties, initial_block_time, initial_hash_rates)
        return

#%% Class: BLOCKCHAIN - #Old - to fix
class BLOCKCHAIN:
    __instance = None
    def __init__(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates, use_geometric_mean):
        self.noAlgos = noAlgos
        self.chain = []
        self.target_difficulties = [[] for i in range(self.noAlgos)]
        self.achieved_difficulties = [[] for i in range(self.noAlgos)]
        self.accumulated_difficulties = [[] for i in range(self.noAlgos)]
        self.block_times = [[] for i in range(self.noAlgos)]
        self.hash_rates = [[] for i in range(self.noAlgos)]
        self.use_geometric_mean = use_geometric_mean
        for i in range(self.noAlgos):
            self.target_difficulties[i].append(initial_difficulties[i])
            self.achieved_difficulties[i].append(initial_difficulties[i])
            self.accumulated_difficulties[i].append(initial_difficulties[i])
            self.block_times[i].append(initial_block_time)
            self.hash_rates[i].append(initial_hash_rates[i])

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

    def get_geometric_mean(self):
        geometric_mean = []
        for i in range(0, len(self.chain)):
            geometric_mean.append(self.chain[i].geometric_mean)
        return geometric_mean

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
        #Determine accumulated difficulties (geometric mean) for all competing algorithms
        geometric_mean = calc_geometric_mean(self.noAlgos, self.accumulated_difficulties, achieved_difficulties)
        #Select algorithm with highest accumulated difficulty or quickest block time
        if self.use_geometric_mean == True:
            algo = geometric_mean.index(max(geometric_mean))
        else:
            algo = block_times.index(min(block_times))
        #Add new block to the blockchain
        accumulated_difficulty = self.accumulated_difficulties[algo][-1] + \
            achieved_difficulties[algo]
        self.chain.append(BLOCK(len(self.chain), algo, achieved_difficulties[algo], accumulated_difficulty, \
                           geometric_mean[algo], block_times[algo], block_times[algo]/self.noAlgos, hash_rates[algo]))
        #Update blockchain stats
        self.target_difficulties[algo].append(target_difficulties[algo])
        self.achieved_difficulties[algo].append(achieved_difficulties[algo])
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
_BT0 = c.incr() #Target block time

#Mining algorithm choices (as per '../other/multi_pow_algos_approximation.*')
algos = []
algos.append(['Algo 1', 119.12, 0.8809, 1000, 1])
algos.append(['Algo 2', 148.94, 0.8511, 10000, 10])
algos.append(['Algo 3', 198.66, 0.8013, 100000, 100])
algos.append(['Algo 4', 298.25, 0.7018, 1000000, 1000])
algos.append(['Algo 5', 597.99, 0.4020, 10000000, 10000])
algos = list(map(list, zip(*algos))) #data into row-column format

hash_rate_profiles = []
hash_rate_profiles.append([[[50, 100], [1.5, 1.5]], \
                           [[100, 200], [1.5, 0.5]], \
                           [[200, 500], [1.0, 1.0]]]) # Algo 1
hash_rate_profiles.append([[[0, 500], [1, 1]]]) # Algo 2
hash_rate_profiles.append([[[0, 500], [1, 1]]]) # Algo 3
hash_rate_profiles.append([[[0, 500], [1, 1]]]) # Algo 4
hash_rate_profiles.append([[[0, 500], [1, 1]]]) # Algo 5

#%% User inputs
#Read inputs from config file
blocksToSolve = noAlgos = diff_algo = targetBT = difficulty_window = randomness_miner = dist_miner = randomness_hash_rate = \
    dist_hash_rate = ''
config_file = os.getcwd() + os.path.sep + "my_inputs_b.txt"
config_file_start_id = ">>>> Gtd$K46U%JN*X#Vd2 >>>>"
config_file_end_id = "<<<< Gtd$K46U%JN*X#Vd2 <<<<"
if os.path.isfile(config_file):
    with open(config_file,"r") as f:
        fl = f.readlines()
        c.reset()
        if fl[c.incr()].strip() == config_file_start_id.strip() and fl[-1].strip() == config_file_end_id.strip():
            blocksToSolve = int(fl[c.incr()].strip())
            noAlgos = int(fl[c.incr()].strip())
            diff_algo = int(fl[c.incr()].strip())
            targetBT = int(fl[c.incr()].strip())
            difficulty_window = int(fl[c.incr()].strip())
            randomness_miner = float(fl[c.incr()].strip())
            dist_miner = int(fl[c.incr()].strip())
            randomness_hash_rate = float(fl[c.incr()].strip())
            dist_hash_rate = int(fl[c.incr()].strip())

#Get new iputs
blocksToSolve =           limit_down(get_input('Enter number of blocks to solve after initial period   ', \
                                               default=blocksToSolve, my_type='int'), 0)
noAlgos =              limit_up_down(get_input('Enter the number of mining algorithms (1-%s)            ' \
                                               % (len(algos)), default=noAlgos, my_type='int'), 1, len(algos))
diff_algo =            limit_up_down(get_input('Diff algo: LWMA(0), LWMA-1_171206(1), LWMA-1_181127(2) ', \
                                               default=diff_algo, my_type='int',), 0, 2)
targetBT =                limit_down(get_input('Enter the system target block time (>=10)              ', \
                                               default=targetBT, my_type='int'), 10)
difficulty_window =       limit_down(get_input('Enter the difficulty algo window (>=1)                 ', \
                                               default=difficulty_window, my_type='int',), 1)
randomness_miner =     limit_up_down(get_input('Enter the mining randomness factor (0-0.9)             ', \
                                               default=randomness_miner, my_type='float',), 0, 0.9)
if randomness_miner != 0:
    dist_miner =       limit_up_down(get_input('    - Dist: None(0), Uniform(1), Normal(2), Poisson(3) ', \
                                               default=dist_miner, my_type='int',), 0, 3)
else:
    dist_miner = 0
randomness_hash_rate = limit_up_down(get_input('Enter the hash rate randomness factor (0-0.9)          ', \
                                               default=randomness_hash_rate, my_type='float',), 0, 0.9)
if randomness_hash_rate != 0:
    dist_hash_rate =   limit_up_down(get_input('    - Dist: None(0), Uniform(1), Normal(2), Poisson(3) ', \
                                               default=dist_hash_rate, my_type='int',), 0, 3)
else:
    dist_hash_rate = 0

#Write new inputs to config file
with open(config_file,"w+") as f:
    f.write(config_file_start_id + "\n")
    f.write(str(blocksToSolve) + "\n")
    f.write(str(noAlgos) + "\n")
    f.write(str(diff_algo) + "\n")
    f.write(str(targetBT) + "\n")
    f.write(str(difficulty_window) + "\n")
    f.write(str(randomness_miner) + "\n")
    f.write(str(dist_miner) + "\n")
    f.write(str(randomness_hash_rate) + "\n")
    f.write(str(dist_hash_rate) + "\n")
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
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA Basic -----\n')
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20171206(difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA-1 version 2017-12-06 -----\n')
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20181127(difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA-1 version 2018-11-27 -----\n')
else:
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window)
    print('\n\n ----- Using difficulty algorithm: LWMA Basic -----\n')

state = BLOCKCHAIN_STATE(noAlgos=noAlgos, initial_difficulties=data[_DF0], initial_block_time=1, \
                   initial_hash_rates=data[_HR0])
if len(state.chain) > 0:
    state.reset(noAlgos=noAlgos, initial_difficulties=data[_DF0], initial_block_time=1, \
                initial_hash_rates=data[_HR0])
miners = []
for i in range(0, noAlgos):
    hash_rate = HASH_RATE(initial_hash_rate=algos[_HR0][i], profile=hash_rate_profiles[i], \
                          randomness=randomness_hash_rate, dist='poisson', name=algos[_NAM][i])
    miners.append(MINER(randomness_miner=randomness_miner, dist='poisson', initial_difficulty=algos[_DF0][i], \
                        initial_block_time=targetBT, gradient=algos[_GRA][i], intercept=algos[_INT][i], \
                        name=algos[_NAM][i], algo_no=i, diff_algo=diff_algo, target_time=targetBT, state=state))

#Old - to fix
chain = BLOCKCHAIN(noAlgos=noAlgos, initial_difficulties=data[_DF0], initial_block_time=1, \
                   initial_hash_rates=data[_HR0], use_geometric_mean=True)

#For debugging
miners_vars = []
for i in range(0, noAlgos):
    miners_vars.append(vars(miners[i]))
chain_vars = vars(chain)
state_vars = vars(state)

#%% Blockchain runtime
#Initial: Adjusting difficulty to achieve target block time

#Scenario starts here

#%% Plot results

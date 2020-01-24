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

#%% Class: ERROR
# Base class for other exceptions
class ERROR(Exception):
   pass

#%% Class: COUNTER
class COUNTER:
    def __init__(self, initial_value=0, increment=1):
        self.new = np.int64(initial_value)
        self.old = np.int64(initial_value)
        self.initial_value = np.int64(initial_value)
        self.increment = np.int64(increment)

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
        self.difficulty_window = abs(difficulty_window)

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
        self.difficulty_window = abs(difficulty_window)

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
        self.difficulty_window = abs(difficulty_window)

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
    def __init__(self, hash_rate_attack, hash_rate_trigger, contest_tip):
        self.hash_rate_attack = bool(hash_rate_attack)
        self.contest_tip = bool(contest_tip)
        self.hash_rate_trigger = float(limit_down(hash_rate_trigger, 1))
        #Internal
        self.selfish_mining = False
        self.selfish_mining_start = False
        self.send_blocks = False

#%% Class: MINER
class MINER:
    def __init__(self, randomness_miner, dist, initial_difficulty, initial_block_time, gradient, intercept, name, algo_no, \
                 diff_algo, target_time, strategy, hash_rate, state):
        self.rand = RANDOM_FUNC(randomness_miner, dist, name, 'miner')
        self.gradient = gradient
        self.intercept = intercept
        self.name = name
        self.algo_no = algo_no
        if str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_00'>" and \
            str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_01_20171206'>" and \
            str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_01_20181127'>":
                raise ERROR('"diff_algo" wrong type: ' + str(type(diff_algo)))
        else:
            self.diff_algo = diff_algo
        self.target_time = target_time
        self.count = COUNTER(initial_value=0, increment=1)
        self.block_hash = BLOCK_HASH()
        self.blocks = []
        if str(type(strategy)) != "<class '__main__.MINE_STRATEGY'>":
            raise ERROR('"strategy" wrong type: ' + str(type(state)))
        else:
            self.strategy = strategy
        if str(type(hash_rate)) != "<class '__main__.HASH_RATE'>":
            raise ERROR('"hash_rate" wrong type: ' + str(type(hash_rate)))
        else:
            self.hash_rate = hash_rate
        if str(type(state)) != "<class '__main__.BLOCKCHAIN_STATE'>":
            raise ERROR('"state" wrong type: ' + str(type(state)))
        else:
            self.state = state
        self.state.chain.append(self.create_block(self.state.target_difficulties[algo_no][-1], \
                                                  self.state.achieved_difficulties[algo_no][-1], self.block_hash.get_next_hash(), \
                                                      algo_no, True))
        #Internal
        self.selfish_mining = False
        self.selfish_mining_start = False
        self.block_number = -1

    def create_block(self, target_difficulty, accumulated_difficulty, previous_hash, block_number, init):
        #Solve time based on ratio between target difficulty and available hash rate
        self.count.reset()
        hash_rate = self.hash_rate.get_hash_rate(block_number, init)
        while self.count.incr() <= 10:
            gradient_r = self.rand.get_value(self.gradient)
            intercept_r = self.rand.get_value(self.intercept)
            solve_time = limit_down((target_difficulty/hash_rate) * gradient_r + intercept_r, 1)
            achieved_difficulty = target_difficulty + (target_difficulty - ((solve_time - self.intercept) / self.gradient) * \
                                                       hash_rate)
            if achieved_difficulty >= target_difficulty:
                break
        else:
            achieved_difficulty = target_difficulty
            solve_time = limit_down((target_difficulty/hash_rate) * self.gradient + self.intercept, 1)
        #Block meta data
        block_hash = self.block_hash.get_next_hash()
        accumulated_difficulty_ = accumulated_difficulty + achieved_difficulty
        block = BLOCK(block_number, block_hash, previous_hash, self.algo_no, target_difficulty, achieved_difficulty, \
                      accumulated_difficulty_, hash_rate, solve_time)
        return block

    def produce_next_blocks(self, block_number, time_now, init):
        #Apply mining strategy
        if self.strategy.hash_rate_attack == True and init == False and self.selfish_mining == False:
            if self.hash_rate.get_hash_rate(block_number, init) >= self.hash_rate.get_hash_rate(block_number-1, init) * \
                self.strategy.hash_rate_trigger:
                    self.strategy.selfish_mining = True
                    self.strategy.send_blocks = False
                    self.strategy.selfish_mining_start = True
        #Produce next blocks
        # - Selfish mining start
        if self.strategy.selfish_mining == True and self.strategy.selfish_mining_start == True:
            self.blocks.clear()
            blockchain_tip = self.state.chain[-1].block_hash
            n_ = self.diff_algo.difficulty_window if len(self.state.chain) > self.diff_algo.difficulty_window else \
                len(self.state.chain)
            n = len(self.state.solve_times[self.algo_no]) - n_
            achieved_difficulties = self.state.achieved_difficulties[self.algo_no][n:]
            accumulated_difficulties = self.state.accumulated_difficulties[self.algo_no][n:]
            solve_times = self.state.solve_times[self.algo_no][n:]
            block_number_ = block_number
            while len(self.blocks) < self.diff_algo.difficulty_window * 0.9:
                target_difficulty = self.diff_algo.adjust_difficulty(achieved_difficulties,  accumulated_difficulties, \
                                                                     solve_times, self.target_time)
                self.blocks.append(self.create_block(target_difficulty, accumulated_difficulties[-1], blockchain_tip, \
                                                     block_number_, init))
                blockchain_tip = self.blocks[-1].block_hash
                achieved_difficulties.append(self.blocks[-1].achieved_difficulty)
                accumulated_difficulties.append(self.blocks[-1].accumulated_difficulty)
                solve_times.append(self.blocks[-1].solve_time)
                block_number_ += 1
            self.block_number = block_number_
            self.strategy.selfish_mining_start = False
            print(self.name, 'selfish_mining')
        # - Normal operation
        elif self.strategy.selfish_mining == False and self.block_number < block_number:
            self.blocks.clear()
            blockchain_tip = self.state.chain[-1].block_hash
            target_difficulty = self.diff_algo.adjust_difficulty(self.state.achieved_difficulties[self.algo_no],
                                                                 self.state.accumulated_difficulties[self.algo_no], \
                                                                 self.state.solve_times[self.algo_no], self.target_time)
            self.blocks.append(self.create_block(target_difficulty, self.state.accumulated_difficulties[self.algo_no][-1], \
                                                 blockchain_tip, block_number, init))
            self.block_number = block_number

        # Wait for system time to catch up with accumulated selfish mining time, then set flag to send blocks array to oracle
        if self.strategy.selfish_mining == True:
            index = self.state.get_block_index(self.blocks[0].previous_hash)
            selfish_mining_time = self.state.chain[index].time_stamp + sum([ x.block_time for x in self.blocks ])
            if time_now >= selfish_mining_time:
                self.strategy.send_blocks = True
            print(self.name, 'self.strategy.send_blocks = True')

        #Send block(s) to oracle
        if self.strategy.selfish_mining == False:
            if self.block_number == block_number:
                return self.blocks
            else:
                print(self.name, 'self.strategy.selfish_mining == False', 'return empty blocks')
                return []
        elif self.strategy.send_blocks == True:
            print(self.name, 'strategy.send_blocks')
            self.strategy.selfish_mining = False
            self.strategy.send_blocks = False
            return self.blocks
        else:
            print(self.name, 'self.strategy.selfish_mining == True', 'return empty blocks')
            return []


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
    def __init__(self, block_number, block_hash, previous_hash, algo, target_difficulty, achieved_difficulty, \
                 accumulated_difficulty, hash_rate, solve_time):
        self.algo = int(algo)
        self.target_difficulty = target_difficulty
        self.achieved_difficulty = float(achieved_difficulty)
        self.accumulated_difficulty = float(accumulated_difficulty)
        self.solve_time = float(solve_time)
        self.hash_rate = float(hash_rate)
        self.block_number = np.uint64(block_number)
        self.block_hash = np.uint64(block_hash)
        self.previous_hash = np.uint64(previous_hash)
        self.geometric_mean = float(0)
        self.block_time = float(0)
        self.time_stamp = float(0)

    def finalize(self, block_time, time_stamp):
        self.block_time = float(block_time)
        self.time_stamp = float(time_stamp)


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
            self.solve_times = [[] for i in range(self.noAlgos)]
            self.hash_rates = [[] for i in range(self.noAlgos)]
            self.system_time = initial_block_time
            for i in range(self.noAlgos):
                self.target_difficulties[i].append(initial_difficulties[i])
                self.achieved_difficulties[i].append(initial_difficulties[i])
                self.accumulated_difficulties[i].append(initial_difficulties[i])
                self.solve_times[i].append(initial_block_time)
                self.hash_rates[i].append(initial_hash_rates[i])

    def reset(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates):
        BLOCKCHAIN_STATE.__instance = None
        BLOCKCHAIN_STATE(noAlgos, initial_difficulties, initial_block_time, initial_hash_rates)
        return

    def update(self, block):
        block_time = block.solve_time #/self.noAlgos
        self.system_time = self.chain[-1].time_stamp + block_time
        block.finalize(block_time, self.system_time)
        self.chain.append(block)
        #Update blockchain stats
        self.target_difficulties[block.algo].append(block.target_difficulty)
        self.achieved_difficulties[block.algo].append(block.achieved_difficulty)
        self.accumulated_difficulties[block.algo].append(block.accumulated_difficulty)
        self.solve_times[block.algo].append(block.solve_time)
        self.hash_rates[block.algo].append(block.hash_rate)
        return

    def get_achieved_difficulties(self):
        return [ x.achieved_difficulty for x in state.chain ]

    def get_accumulated_difficulties(self):
        return [ x.accumulated_difficulty for x in state.chain ]

    def get_geometric_mean(self):
        return [ x.geometric_mean for x in state.chain ]

    def get_block_times(self):
        return [ x.block_time for x in state.chain ]

    def get_hash_rates(self):
        return [ x.hash_rate for x in state.chain ]

    def get_block_hash(self):
        return [ x.block_hash for x in state.chain ]

    def get_block_index(self, block_hash):
        try:
            return [ x.block_hash for x in state.chain ].index(block_hash)
        except ValueError:
            return -1

    def get_algo(self):
        return [ x.algo for x in state.chain ]

    def count_repeats(self):
        #Count repeats
        repeats = []
        counts = [1 for i in range(self.noAlgos)]
        for i in range(1, len(self.chain)):
            if (self.chain[i].algo == self.chain[i-1].algo) and (i < len(self.chain)-1):
                counts[self.chain[i].algo] += 1
            else:
                repeats.append([i-1, self.chain[i-1].algo, counts[self.chain[i-1].algo]])
                counts[self.chain[i-1].algo] = 1
        repeats = list(map(list, zip(*repeats))) #data into row-column format
        return repeats


#%% Class: ORACLE
class ORACLE():
    def __init__(self, state, use_geometric_mean):
        if str(type(state)) != "<class '__main__.BLOCKCHAIN_STATE'>":
            raise ERROR('"state" wrong type: ' + str(type(state)))
        else:
            self.state = state
        self.use_geometric_mean = use_geometric_mean

    def get_new_blocks(self):
        return

    def run(self, miners, blocks_amount, init):
        for i in range(self.state.noAlgos, blocks_amount):
            #Get blocks for current round (no reorgs)
            blocks = [[] for i in range(self.state.noAlgos)]
            time = [[],[]]
            for j in range(0, len(miners)):
                blocks[j] = miners[j].produce_next_blocks(i, self.state.system_time, init)
                #Log individual solve times for valid blocks
                if len(blocks[j]) == 1:
                    if blocks[j][-1].previous_hash == self.state.chain[-1].block_hash:
                        time[0].append(j)
                        time[1].append(blocks[j][-1].solve_time)
            #Add block with quickest solve time to the blockchain
            if len(time[0]) > 0:
                algo = time[0][time[1].index(min(time[1]))] #Quickest time
                winning_block = blocks[algo]
                self.state.update(blocks[algo][-1])
            else:
                algo = -1
                self.state.system_time = self.chain[-1].time_stamp + self.state.target_time
            print('time:', time[1], '  system_time:', self.state.system_time)
            #Give opportunity for re-org based on geometric mean of contending algos
            if len(time[0]) > 1:
                blocks = [[] for i in range(self.state.noAlgos)]
                for j in range(0, len(miners)):
                    if j == algo:
                        blocks[j] = winning_block
                    else:
                        blocks[j] = miners[j].produce_next_blocks(i, self.state.system_time + max(time[1]) * 1.01, init)
                # prepare data for geometric mean calc
                accumulated_difficulties = []
                for i in range(len(self.state.accumulated_difficulties)):
                    accumulated_difficulties.append(self.state.accumulated_difficulties[i][-1])
                achieved_difficulties = []
                for i in range(len(self.state.achieved_difficulties)):
                    achieved_difficulties.append(self.state.achieved_difficulties[i][-1])
                # perform geometric mean calc
                geometric_mean = calc_geometric_mean(self.state.noAlgos, accumulated_difficulties, achieved_difficulties)
                print('geo_mean:', geometric_mean)
                # reoerg to required depth if applicable
                #??
        return

    def add_block(self, block_times, target_difficulties, achieved_difficulties, hash_rates, init=False):
        #Determine accumulated difficulties (geometric mean) for all competing algorithms
        accumulated_difficulties = []
        for i in range(len(self.accumulated_difficulties)):
            accumulated_difficulties.append(self.accumulated_difficulties[i][-1])
        geometric_mean = calc_geometric_mean(self.state.noAlgos, accumulated_difficulties, achieved_difficulties)
        #Select algorithm with highest accumulated difficulty or quickest block time
        if self.use_geometric_mean == True:
            algo = geometric_mean.index(max(geometric_mean))
        else:
            algo = block_times.index(min(block_times))
        #Add new block to the blockchain
        accumulated_difficulty = self.state.accumulated_difficulties[algo][-1] + \
            achieved_difficulties[algo]
        self.state.chain.append(BLOCK(len(self.state.chain), algo, target_difficulties[algo], achieved_difficulties[algo], \
                                      accumulated_difficulty, geometric_mean[algo], block_times[algo], \
                                      block_times[algo]/self.state.noAlgos, hash_rates[algo]))
        #Update blockchain stats
        self.state.target_difficulties[algo].append(target_difficulties[algo])
        self.state.achieved_difficulties[algo].append(achieved_difficulties[algo])
        self.state.accumulated_difficulties[algo].append(accumulated_difficulty)
        self.state.block_times[algo].append(block_times[algo])
        self.state.hash_rates[algo].append(hash_rates[algo])

    def broadcast_time():
        #ToDo: Update system time at every reported block solve time
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

#Blockchain state, eshared among all miners and oracle
state = BLOCKCHAIN_STATE(noAlgos=noAlgos, initial_difficulties=algos[_DF0], initial_block_time=1, initial_hash_rates=algos[_HR0])
if len(state.chain) > 0:
    state.reset(noAlgos=noAlgos, initial_difficulties=algos[_DF0], initial_block_time=1, initial_hash_rates=algos[_HR0])

#Mining strategies
strategies = []
strategies.append(MINE_STRATEGY(hash_rate_attack=True, hash_rate_trigger=1.5, contest_tip=False))
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, contest_tip=True))
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, contest_tip=False))

#Miners
miners = []
for i in range(0, noAlgos):
    hash_rate = HASH_RATE(initial_hash_rate=algos[_HR0][i], profile=hash_rate_profiles[i], \
                          randomness=randomness_hash_rate, dist='poisson', name=algos[_NAM][i])
    miners.append(MINER(randomness_miner=randomness_miner, dist='poisson', initial_difficulty=algos[_DF0][i], \
                        initial_block_time=targetBT, gradient=algos[_GRA][i], intercept=algos[_INT][i], name=algos[_NAM][i], \
                        algo_no=i, diff_algo=diff_algo, target_time=targetBT, strategy=strategies[i], hash_rate=hash_rate, \
                        state=state))

#Oracle
oracle = ORACLE(state=state, use_geometric_mean=True)

#For debugging
miners_vars = []
for i in range(0, noAlgos):
    miners_vars.append(vars(miners[i]))
oracle_vars = vars(oracle)
state_vars = vars(state)

#%% Blockchain runtime
#Initial: Adjusting difficulty to achieve target block time
settling_window = int(abs(diff_algo.difficulty_window*1.5*noAlgos))
oracle.run(miners=miners, blocks_amount=settling_window, init=True)
#Scenario starts here
oracle.run(miners=miners, blocks_amount=blocksToSolve, init=False)


#%% Plot results


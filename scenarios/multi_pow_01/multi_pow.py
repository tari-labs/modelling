import matplotlib.pyplot as plt
import numpy as np
import heapq
import os
import copy
from itertools import cycle
from itertools import combinations

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

#%% get_distribution_text
def get_distribution_text(value):
    if value == 0:
        return 'none'
    elif value == 1:
        return 'uniform'
    elif value == 2:
        return 'normal'
    elif value == 3:
        return 'poisson'

#%% calc_geometric_mean
# Geometric mean (overflow resistant)
def calc_geometric_mean(values):
    try:
        n = len(values)
    except:
        print('Error: "def calc_geometric_mean(values)": One dimensional list or array required.')
        return 0.0
    geometric_mean = 0.0
    for j in range(0, n):
        geometric_mean +=  np.log(values[j])
    try:
        geometric_mean = np.exp(geometric_mean/n)
    except:
        print('Error: "def calc_geometric_mean(values)": Division by zero, zero length array/list provided.')
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

    def reset(self):
        self.new = self.initial_value
        self.old = self.initial_value

    def incr(self):
        self.old = self.new
        self.new += self.increment
        return self.old

    def decr(self):
        self.old = self.new
        self.new -= self.increment
        return self.old

    def val(self):
        return self.old

#%% Class: DIFFICULTY_LWMA_00
#Linear Weighted Moving Average - Basic
class DIFFICULTY_LWMA_00:
    def __init__(self, difficulty_window):
        self.difficulty_window = abs(difficulty_window)
        print(' ----- Using difficulty algorithm: LWMA Basic -----')

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time, current_time, previous_time_stamp):
        #Not used: current_time, previous_time_stamp
        n = self.difficulty_window if len(solve_times) > self.difficulty_window else len(solve_times)
        avg_diff = np.mean(difficulties[len(difficulties)-n:])
        _sum = 0
        denom = 0
        for i in range(len(solve_times)-n, len(solve_times)):
            _sum += (solve_times[i] * (i+1))
            denom += (i+1)
        return np.int64(avg_diff * (target_time/(_sum/denom)))

#%% Class: DIFFICULTY_LWMA_01_20171206
#Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2017-12-06
#(https://github.com/zawy12/difficulty-algorithms/issues/3#issue-279773112)
class DIFFICULTY_LWMA_01_20171206:
    def __init__(self, difficulty_window):
        self.difficulty_window = abs(difficulty_window)
        print(' ----- Using difficulty algorithm: LWMA-1 version 2017-12-06 -----')

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time, current_time, previous_time_stamp):
        #Not used: current_time, previous_time_stamp
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
        return  np.int64(next_D)

#%% Class: DIFFICULTY_LWMA_01_20181127
#Linear Weighted Moving Average - Bitcoin & Zcash Clones - 2018-11-27
#( https://github.com/zawy12/difficulty-algorithms/issues/3#issuecomment-442129791 )
#( https://github.com/tari-project/tari/blob/development/base_layer/core/src/proof_of_work/lwma_diff.rs )
class DIFFICULTY_LWMA_01_20181127:
    def __init__(self, difficulty_window):
        self.difficulty_window = abs(difficulty_window)
        print(' ----- Using difficulty algorithm: LWMA-1 version 2018-11-27 -----')

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time, current_time, previous_time_stamp):
        #Not used: current_time, previous_time_stamp
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
        return  np.int64(target)

#%% Class: DIFFICULTY_TSA_20181108
#TSA, Time Stamp Adjustment to Difficulty, Copyright (c) 2018 Zawy, MIT License.
#( https://github.com/zawy12/difficulty-algorithms/issues/36 )
class DIFFICULTY_TSA_20181108:
    def __init__(self, difficulty_window):
        self.difficulty_window = abs(difficulty_window)
        self.k = 1E3
        self.M = 6.5 # M can from 3 (aggressive) to 5 (conservative) to 10 (slow)
        self.lwma = DIFFICULTY_LWMA_01_20181127(self.difficulty_window)
        print('               with')
        print(' ----- Using difficulty algorithm: TSA version 2018-11-08 [(c) 2018 Zawy]-----')

    def adjust_difficulty(self, difficulties, acc_difficulties, solve_times, target_time, current_time, previous_time_stamp):
        TSA_D = self.lwma.adjust_difficulty(difficulties, acc_difficulties, solve_times, target_time, current_time,
                                            previous_time_stamp)

        TM = target_time*self.M
        exk = self.k
        current_solve_time_estimate = max(1, max(solve_times[-1], current_time - previous_time_stamp))
        solve_time = np.int64(min(current_solve_time_estimate, 6*target_time))
        for i in range(1, np.int64(solve_time/TM)):
            exk = (exk*np.int64(2.718*self.k))/self.k
        f = solve_time % TM
        exk = (exk*(self.k+(f*(self.k+(f*(self.k+(f*self.k)/(3*TM)))/(2*TM)))/(TM)))/self.k
        TSA_D = max(np.int64(10), (TSA_D*((1000*(self.k*solve_time))/(self.k*target_time+(solve_time-target_time)*exk)))/1000)
        j = 1000000000
        while j > 1:
            if TSA_D > j*100:
                TSA_D = ((TSA_D+j/2)/j)*j
                break
            else:
                j /= 10
        if self.M == 1:
            TSA_D = (TSA_D*85)/100
        elif self.M == 2:
            TSA_D = (TSA_D*95)/100
        elif self.M == 3:
            TSA_D = (TSA_D*99)/100

        return np.int64(TSA_D)

#%% Class: RANDOM_FUNC
class RANDOM_FUNC:
    def __init__(self, randomness, distribution, name, owner):
        self.randomness = limit_up_down(randomness, 0, 0.9)
        self.rand_down = (1 - self.randomness)
        self.rand_up = (1 + self.randomness)

        if str(distribution) == 'none':
            self.distribution = 'none'
            print(' ----- %s: Randomness %s => none\n' % (name, owner))
        else:
            if str(distribution) == 'poisson':
                self.distribution = 'poisson'
                print(' ----- %s: Randomness %s => poisson distribution\n' % (name, owner))
            elif self.randomness > 0:
                if str(distribution) == 'normal': #'uniform' or 'normal' or 'poisson'
                    self.distribution = 'normal'
                    print(' ----- %s: Randomness %s => normal distribution, at %s\n' % (name, owner, self.randomness * 100))
                elif str(distribution) == 'uniform':
                    self.distribution = 'uniform'
                    print(' ----- %s: Randomness %s => uniform distribution, at +/- %s\n' % (name, owner, self.randomness * 100))
                else:
                    self.distribution = 'none'
                    print(' ----- %s: Randomness %s => none\n' % (name, owner))
            else:
                self.distribution = 'none'
                print(' ----- %s: Randomness %s => none\n' % (name, owner))

    def get_value(self, value):
        if self.distribution == 'normal':
            value = np.random.normal(value, value*self.randomness, 1)
        elif self.distribution == 'poisson':
            value = np.random.poisson(value, 1)
        elif self.distribution == 'uniform':
            value = np.random.uniform(value*self.rand_down, value*self.rand_up)
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
    def __init__(self, hash_rate_attack, hash_rate_trigger, self_mine_factor, contest_tip):
        self.hash_rate_attack = bool(hash_rate_attack)
        self.contest_tip = bool(contest_tip)
        self.hash_rate_trigger = float(limit_down(hash_rate_trigger, 1))
        self.self_mine_factor = float(limit_down(self_mine_factor, 0))
        #Internal
        self.selfish_mining = False
        self.selfish_mining_start = False
        self.send_blocks = False

#%% Class: MINER
class MINER:
    def __init__(self, randomness_miner, dist, initial_difficulty, gradient, intercept, name, algo_no, \
                 diff_algo, strategy, hash_rate, state):
        self.rand = RANDOM_FUNC(randomness_miner, dist, name, 'miner')
        self.gradient = gradient
        self.intercept = intercept
        self.name = name
        self.algo_no = algo_no
        self.min_delta_time = 0 #state.miner_target_time[algo_no] / 10 # This is just a guess, used if the algo lags
        self.new_block_overhead_time = state.miner_target_time[algo_no] / 100 # This is just a guess, used if a cycle is skipped
        if str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_00'>" and \
            str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_01_20171206'>" and \
            str(type(diff_algo)) != "<class '__main__.DIFFICULTY_LWMA_01_20181127'>" and \
            str(type(diff_algo)) != "<class '__main__.DIFFICULTY_TSA_20181108'>":
                raise ERROR('"diff_algo" wrong type: ' + str(type(diff_algo)))
        else:
            self.diff_algo = diff_algo
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
        self.state.chain.append(self.create_block(self.state.target_difficulties[algo_no][-1],
                                                  self.state.achieved_difficulties[algo_no][-1], self.block_hash.get_next_hash(),
                                                  0, 0, algo_no, True))
        #Internal
        self.block_number = -1
        self.selfish_mining_time = 0
        self.block_number_selfish_mining_start = -1

    def create_block(self, target_difficulty, accumulated_difficulty, previous_hash, time_now, previous_time_stamp, \
                     block_number, init):
        #Solve time based on ratio between target difficulty and available hash rate
        self.count.reset()
        hash_rate = self.hash_rate.get_hash_rate(block_number, init)
        while self.count.incr() <= 50:
            #Randomness can influence the achieved difficulty
            gradient_r = self.rand.get_value(self.gradient)
            solve_time = limit_down((target_difficulty/hash_rate) * gradient_r + self.intercept, 1)
            achieved_difficulty = np.ceil(((solve_time - self.intercept) / self.gradient) * hash_rate)
            #Randomness can influence the solve time
            solve_time = self.rand.get_value(solve_time)
            #Target difficulty must always be achievd
            if achieved_difficulty >= target_difficulty:
                break
        else:
            print('Could not attain target difficulty at block', block_number, 'for', self.name)
            print('                         adjusted solve time', solve_time, 'and achieved_difficulty', achieved_difficulty)
            achieved_difficulty = target_difficulty
            solve_time = limit_down((target_difficulty/hash_rate) * self.gradient + self.intercept, 1)
            print('                               to solve time', solve_time, 'and achieved_difficulty', achieved_difficulty)
        # - Add overhead time if an algo lagged to simulate discarding the current block for the new block to solve
        if len(self.state.chain) > 0:
            if self.algo_no != self.state.chain[-1].algo:
                solve_time = solve_time + self.new_block_overhead_time
        #Compensate for the time warp due to difference in oracle's "time now" and this algo's "previous time stamp"
        #     This solution is based on the average time it takes to produce a block, thus not random based
        #     'delta_time' will be used to increment the oracle's time
        #     'delta_time' should thus continue from this algo's previous time stamp, not from the time another algo produced
        #     a block, i.e. the oracle's time
        # - The time lag will be subtracted from the solve time to simulate probability of solving the block in a longer time
#        lag = max((time_now - previous_time_stamp) - self.state.miner_target_time[self.algo_no], 0)
        lag = time_now - previous_time_stamp
        delta_time = max(self.min_delta_time, solve_time - lag)
        #Block meta data
        block_hash = self.block_hash.get_next_hash()
        accumulated_difficulty_ = accumulated_difficulty + achieved_difficulty
        block = BLOCK(block_number, block_hash, previous_hash, self.algo_no, self.name, target_difficulty, achieved_difficulty,
                      accumulated_difficulty_, hash_rate, delta_time, solve_time)
        return block

    def produce_next_blocks(self, block_number, time_now, init, contest_mode):
        # Apply mining strategy
        previous_time_stamp = self.state.chain[self.state.get_algo_last_index(self.algo_no)].time_stamp
        if self.strategy.hash_rate_attack == True and init == False and self.strategy.selfish_mining == False:
            if self.hash_rate.get_hash_rate(block_number, init) >= self.hash_rate.get_hash_rate(block_number-1, init) * \
                self.strategy.hash_rate_trigger:
                    self.strategy.selfish_mining = True
                    self.strategy.send_blocks = False
                    self.strategy.selfish_mining_start = True
                    print('\nMiner: ', self.name, ': selfish_mining trigger', ', contest_tip', self.strategy.contest_tip,
                          ', hash_rate: (n-1)', round(self.hash_rate.get_hash_rate(block_number-1, init), 0), '(n)',
                          round(self.hash_rate.get_hash_rate(block_number, init), 0), ', block', block_number, ', time_now',
                          time_now)
        # Produce next blocks
        #  - Normal operation
        if self.strategy.selfish_mining == False and self.block_number < block_number:
            self.blocks.clear()
            blockchain_tip = self.state.chain[-1].block_hash
            target_difficulty = self.diff_algo.adjust_difficulty(self.state.achieved_difficulties[self.algo_no],
                                        self.state.accumulated_difficulties[self.algo_no],
                                        self.state.solve_times[self.algo_no], self.state.miner_target_time[self.algo_no],
                                        time_now, previous_time_stamp)
            self.blocks.append(self.create_block(target_difficulty, self.state.accumulated_difficulties[self.algo_no][-1],
                                                 blockchain_tip, time_now, previous_time_stamp, block_number, init))
            self.block_number = block_number
            self.strategy.send_blocks = True

        #  - Selfish mining
        elif self.strategy.selfish_mining == True and self.strategy.selfish_mining_start == True:
            self.blocks.clear()
            blockchain_tip = self.state.chain[-1].block_hash
            achieved_difficulties = copy.deepcopy(self.state.achieved_difficulties[self.algo_no])
            accumulated_difficulties = copy.deepcopy(self.state.accumulated_difficulties[self.algo_no])
            solve_times = copy.deepcopy(self.state.solve_times[self.algo_no])
            self.block_number_selfish_mining_start = block_number
            block_number_ = block_number
            while len(self.blocks) < self.diff_algo.difficulty_window * self.strategy.self_mine_factor:
                time_now_ = time_now + sum([x.solve_time for x in self.blocks])
                target_difficulty = self.diff_algo.adjust_difficulty(achieved_difficulties,  accumulated_difficulties,
                                                                     solve_times, self.state.miner_target_time[self.algo_no],
                                                                     time_now_, previous_time_stamp)
                self.blocks.append(self.create_block(target_difficulty, accumulated_difficulties[-1], blockchain_tip,
                                                     time_now, previous_time_stamp, block_number_, init))
                blockchain_tip = self.blocks[-1].block_hash
                achieved_difficulties.append(self.blocks[-1].achieved_difficulty)
                accumulated_difficulties.append(self.blocks[-1].accumulated_difficulty)
                solve_times.append(self.blocks[-1].solve_time)
                #print('Miner: ', self.name, ':', achieved_difficulties[-1], accumulated_difficulties[-1], \
                #      solve_times[-1], block_number_)
                previous_time_stamp = time_now_
                block_number_ += 1
            self.block_number = block_number_
            index = self.state.get_block_index(self.blocks[0].previous_hash)
            self.selfish_mining_time = self.state.chain[index].time_stamp + sum([x.solve_time for x in self.blocks])
            self.strategy.selfish_mining_start = False
            print('Miner: ', self.name, ':', 'selfish_mining', len(self.blocks), 'blocks, wait till',
                  self.selfish_mining_time, 'to send blocks')

        # Wait for system time to catch up with accumulated selfish mining time, then set flag to send blocks array to oracle
        if self.strategy.selfish_mining == True:
            if time_now >= self.selfish_mining_time and contest_mode == True:
                self.strategy.send_blocks = True

        # Send block(s) to oracle
        if self.strategy.selfish_mining == False: # and self.strategy.contest_tip == False:
            if self.strategy.send_blocks == True:
                self.strategy.send_blocks = False
                #print('\nMiner: ', self.name, ', block', block_number, ', solve_time', self.blocks[-1].solve_time)
                return self.blocks
            else:
                return []
        elif self.strategy.selfish_mining == True:
            if self.strategy.send_blocks == True:
                print('Miner: ', self.name, ':', 'selfish_mining, sending', len(self.blocks), 'blocks after',
                      block_number-self.block_number_selfish_mining_start, 'blocks, time_now', time_now)
                self.strategy.selfish_mining = False
                self.strategy.send_blocks = False
                self.block_number = -1
                self.selfish_mining_time = 0
                return self.blocks
            else:
                return []
        else:
            print('Miner: ', self.name, ':', 'undefined state - return empty blocks')
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
    def __init__(self, block_number, block_hash, previous_hash, algo, name, target_difficulty, achieved_difficulty, \
                 accumulated_difficulty, hash_rate, delta_time, solve_time):
        self.algo = int(algo)
        self.name = str(name)
        self.target_difficulty = target_difficulty
        self.achieved_difficulty = float(achieved_difficulty)
        self.accumulated_difficulty = float(accumulated_difficulty)
        self.delta_time = round(float(delta_time), 1)
        self.solve_time = round(float(solve_time), 1)
        self.hash_rate = float(hash_rate)
        self.block_number = np.uint64(block_number)
        self.block_hash = np.uint64(block_hash)
        self.previous_hash = np.uint64(previous_hash)
        self.geometric_mean = float(0)
        self.block_time = float(0)
        self.time_stamp = float(0)

    def finalize(self, block_time, time_stamp, geometric_mean):
        self.block_time = round(float(block_time), 1)
        self.time_stamp = round(float(time_stamp), 1)
        self.geometric_mean = geometric_mean


#%% Class: BLOCKCHAIN_SHARED_STATE
#Shared state for the singleton blockchain
class BLOCKCHAIN_STATE_BORG:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state

#%% Class: BLOCKCHAIN_STATE
class BLOCKCHAIN_STATE(BLOCKCHAIN_STATE_BORG):
    __instance = None
    def __init__(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates, blockchain_target_time, \
                 target_time_profile):
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
            self.delta_solve_times = [[] for i in range(self.noAlgos)]
            self.solve_times = [[] for i in range(self.noAlgos)]
            self.hash_rates = [[] for i in range(self.noAlgos)]
            self.blocks = [[] for i in range(self.noAlgos)]
            self.system_time = initial_block_time
            self.blockchain_target_time = blockchain_target_time
            self.miner_target_time = [x * noAlgos * blockchain_target_time for x in target_time_profile]
            self.block_number = -1
            for i in range(self.noAlgos):
                self.target_difficulties[i].append(initial_difficulties[i])
                self.achieved_difficulties[i].append(initial_difficulties[i])
                self.accumulated_difficulties[i].append(initial_difficulties[i])
                self.delta_solve_times[i].append(initial_block_time)
                self.solve_times[i].append(initial_block_time)
                self.hash_rates[i].append(initial_hash_rates[i])
                self.blocks[i].append(0)

    def reset(self, noAlgos, initial_difficulties, initial_block_time, initial_hash_rates, blockchain_target_time, \
              target_time_profile):
        BLOCKCHAIN_STATE.__instance = None
        BLOCKCHAIN_STATE(noAlgos, initial_difficulties, initial_block_time, initial_hash_rates, blockchain_target_time, \
              target_time_profile)
        return

    def get_geometric_mean_data(self, block):
        accumulated_difficulties = [1 for i in range(self.noAlgos)]
        #From the current tip's perspective
        root_index = self.get_block_index(block.previous_hash)
        if root_index < 0:
            return []
        tip = block.algo
        accumulated_difficulties[tip] = block.accumulated_difficulty
        #For the competing algos
        my_range = [i for i in range(self.noAlgos)]
        my_range.pop(my_range.index(tip))
        for i in my_range:
            j = root_index - 1
            while accumulated_difficulties[i] == 1 and j >= 0:
                if self.chain[j].algo == i:
                    accumulated_difficulties[i] = self.chain[j].accumulated_difficulty
                else:
                    j -= 1
        return accumulated_difficulties

    def update(self, block, block_time):
        self.system_time = round(self.chain[-1].time_stamp + block_time, 1)
        accumulated_difficulties = self.get_geometric_mean_data(block)
        geometric_mean = calc_geometric_mean(accumulated_difficulties)
        block.finalize(block_time, self.system_time, geometric_mean)
        self.chain.append(block)
        #Update blockchain stats
        self.target_difficulties[block.algo].append(block.target_difficulty)
        self.achieved_difficulties[block.algo].append(block.achieved_difficulty)
        self.accumulated_difficulties[block.algo].append(block.accumulated_difficulty)
        self.delta_solve_times[block.algo].append(block.delta_time)
        self.solve_times[block.algo].append(block.solve_time)
        self.hash_rates[block.algo].append(block.hash_rate)
        self.blocks[block.algo].append(len(self.chain))
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

    def get_algo_last_index(self, algo):
        try:
            return len(state.chain) - 1 - [x.algo for x in reversed(state.chain)].index(algo)
        except ValueError:
            return 0

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
    def __init__(self, state):
        if str(type(state)) != "<class '__main__.BLOCKCHAIN_STATE'>":
            raise ERROR('"state" wrong type: ' + str(type(state)))
        else:
            self.state = state
        self.min_time = []
        self.init_blocks_count = 0

    def get_geometric_mean_data(self, blocks):
        accumulated_difficulties = [0 for i in range(state.noAlgos)]
        #From the current tip's perspective
        root_index = self.state.get_block_index(blocks[0].previous_hash)
        print('Oracle: root_index is', root_index, 'for geometric mean calc of', blocks[0].name)
        if root_index < 0:
            return []
        tip = blocks[0].algo
        accumulated_difficulties[tip] = blocks[-1].accumulated_difficulty
        #For the competing algos
        my_range = [i for i in range(state.noAlgos)]
        my_range.pop(my_range.index(tip))
        for i in my_range:
            j = root_index - 1
            while accumulated_difficulties[i] == 0 and j >= 0:
                if self.state.chain[j].algo == i:
                    accumulated_difficulties[i] = self.state.chain[j].accumulated_difficulty
                else:
                    j -= 1
        return accumulated_difficulties

    def calc_time(self, time):
        time_r = []
        for i in range(0, len(time)):
            time_c = heapq.nsmallest(len(time)-i, time)
            time_r.append(sum([x for x in time_c])/len(time_c)/len(time_c))
        return round(min(time_r), 1)

    def re_org(self, blocks):
        root_index = self.state.get_block_index(blocks[0].previous_hash)
        print('Oracle: root_index is', root_index, 'for re-org based on', blocks[0].name)
        if root_index < 0:
            return
        while len(self.state.chain) > root_index + 1:
            #print('Oracle: removing block', self.state.chain[-1].block_number, 'with hash', self.state.chain[-1].block_hash, \
            #      'of', self.state.chain[-1].name)
            self.state.chain.pop()
        for i in range(len(blocks)):
            if len(blocks) > 1:
                self.state.update(blocks[i], blocks[i].solve_time)
            else:
                self.state.update(blocks[i], blocks[i].solve_time/self.state.noAlgos)
            #print('Oracle: added block', self.state.chain[-1].block_number, 'with hash', self.state.chain[-1].block_hash, \
            #      'of', self.state.chain[-1].name)
        for i in range(0, len(miners)):
            miners[i].block_number = self.state.chain[-1].block_number

    def run(self, miners, blocks_amount, init):
        self.min_time = []
        blocks_requested = blocks_amount if init == True else blocks_amount + self.init_blocks_count
        cut_off_time = blocks_requested * self.state.blockchain_target_time * 1.1
        while len(self.state.chain) < blocks_requested and self.state.system_time < cut_off_time:
            block_number = int(self.state.chain[-1].block_number) + 1
            # Get blocks for current round (no re-orgs)
            blocks = [[] for k in range(self.state.noAlgos)]
            time = [[], [], []]
            #print('\nOracle: Get blocks for current round (no re-orgs), block number', block_number, ', time',
            #      self.state.system_time)
            for j in range(0, len(miners)):
                blocks[j] = miners[j].produce_next_blocks(block_number, self.state.system_time, init, contest_mode=False)
                #Log individual solve times for valid blocks
                if len(blocks[j]) == 1:
                    if blocks[j][-1].previous_hash == self.state.chain[-1].block_hash:
                        time[0].append(j)
                        time[1].append(blocks[j][-1].delta_time)
                        time[2].append(blocks[j][-1].name)
                elif len(blocks[j]) > 1:
                    print('Received invalid blocks from', blocks[j][-1].name, ' at block', block_number, ' time',
                          self.state.system_time)
            # Add block with quickest solve time to the blockchain
            if len(time[0]) > 0:
                min_time = [k for k, x in enumerate(time[1]) if x == min(time[1])]
                if self.min_time != min_time:
                    self.min_time = min_time
                    min_time_cycle = cycle(min_time)
                algo = time[0][next(min_time_cycle)] #Quickest time, alternate if algos are equal
                block_at_tip = blocks[algo]
                self.state.update(blocks[algo][-1], blocks[algo][-1].delta_time)
                #print('Oracle: times', time[1], ' d_time', delta_time, ' time', self.state.system_time, '  - winner:', \
                #       blocks[algo][-1].name)
            else:
                algo = -1
                self.state.system_time += self.state.blockchain_target_time
            #if len(time[0]) != self.state.noAlgos:
            #    print('\nOracle: solve times', time[2], time[1], 'system_time', self.state.system_time, ', block number', \
            #          block_number)
            # Give opportunity for re-org based on geometric mean of contending algos
            if len(time[0]) > 0:
                # Get re-org blocks for current round (miners not participating will return empty blocks)
                blocks = [[] for k in range(self.state.noAlgos)]
                participants = []
                for j in range(0, len(miners)):
                    if j != algo:
                        blocks[j] = miners[j].produce_next_blocks(block_number, self.state.system_time - min(time[1]) + \
                                                                  max(time[1]) * 1.1, init, contest_mode=True)
                        if len(blocks[j]) > 0:
                            participants.append(j)
                if len(participants) > 0:
                    print('\nOracle: Re-org detected from ', [blocks[k][-1].name for k in participants])
                    blocks[algo] = block_at_tip
                    participants.append(algo)
                    participants.sort()
                    print('Oracle: system_time', self.state.system_time - min(time[1]) + max(time[1]) * 1.01, ', block number', \
                          block_number)
                    print('Oracle: Re-org participants', [blocks[k][-1].name for k in participants])
                # Perform geometric mean calc
                if len(participants) > 0:
                    geometric_mean = [0 for k in range(self.state.noAlgos)]
                    for k in participants:
                        accumulated_difficulties = self.get_geometric_mean_data(blocks[k])
                        print('Oracle: accumulated_difficulties for', blocks[k][-1].name, accumulated_difficulties)
                        geometric_mean[k] = calc_geometric_mean(accumulated_difficulties)
                    winning_algo = geometric_mean.index(max(geometric_mean))
                    print('Oracle: geometric_mean', geometric_mean, ' - winning the race is', blocks[winning_algo][-1].name)
                    # reoerg to required depth if applicable
                    if winning_algo != block_at_tip[0].algo:
                        print('Oracle: Re-org based on', blocks[winning_algo][-1].name)
                        self.re_org(blocks[winning_algo])
        if init == True:
            self.init_blocks_count = blocks_amount


#%% Main program header
#------------------------------------
#            Main Program
#------------------------------------

#%% Mining algo constants
# ---- Identifiers
c = COUNTER(initial_value=0, increment=1)
_NAM = c.incr() #Name
_GRA = c.incr() #Gradient
_INT = c.incr() #Intercept
_HR0 = c.incr() #Initial hash rate
_DF0 = c.incr() #Initial difficulty
_BT0 = c.incr() #Target block time

# ---- Mining algorithm
#Mining algorithm choices (as per './multi_pow_algos_approximation.*')
algos = []
algos.append(['Algo 1', 119.12, 0.8809, 1000, 1])
algos.append(['Algo 2', 148.94, 0.8511, 10000, 10])
algos.append(['Algo 3', 198.66, 0.8013, 100000, 100])
algos.append(['Algo 4', 298.25, 0.7018, 1000000, 1000])
algos.append(['Algo 5', 597.99, 0.4020, 10000000, 10000])
algos = list(map(list, zip(*algos))) #data into row-column format


#%% User inputs
# ---- Read config file
blocksToSolve = noAlgos = diff_algo = targetBT = difficulty_window = randomness_miner = dist_miner = randomness_hash_rate = \
    dist_hash_rate = do_distribution_calc = add_randomness = ''
config_file = os.getcwd() + os.path.sep + "multi_pow_inputs.txt"
config_file_start_id = ">>>> Gtd$K46U%JN*X#Vd4 >>>>"
config_file_end_id = "<<<< Gtd$K46U%JN*X#Vd4 <<<<"
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
            add_randomness = int(fl[c.incr()].strip())
            randomness_miner = float(fl[c.incr()].strip())
            dist_miner = int(fl[c.incr()].strip())
            randomness_hash_rate = float(fl[c.incr()].strip())
            dist_hash_rate = int(fl[c.incr()].strip())
            do_distribution_calc = int(fl[c.incr()].strip())

# ---- Get new iputs
blocksToSolve =           limit_down(get_input('Enter number of blocks to solve after initial period       ', \
                                               default=blocksToSolve, my_type='int'), 0)
noAlgos =              limit_up_down(get_input('Enter the number of mining algorithms (1-%s)                ' \
                                               % (len(algos)), default=noAlgos, my_type='int'), 1, len(algos))
diff_algo =            limit_up_down(get_input('Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     ', \
                                               default=diff_algo, my_type='int',), 0, 3)
targetBT =                limit_down(get_input('Enter the system target block time (>=10)                  ', \
                                               default=targetBT, my_type='int'), 10)
difficulty_window =       limit_down(get_input('Enter the difficulty algo window (>=1)                     ', \
                                               default=difficulty_window, my_type='int',), 1)
add_randomness =       limit_up_down(get_input('Add randomness? (0=False/1=True)                           ', \
                                               default=add_randomness, my_type='int',), 0, 1)

if add_randomness == 1:
    dist_miner =       limit_up_down(get_input(' - Mining dist: None(0), Uniform(1), Normal(2), Poisson(3) ', \
                                               default=dist_miner, my_type='int',), 0, 3)
    if dist_miner != 0 and dist_miner != 3:
        randomness_miner = \
                       limit_up_down(get_input('        - mining randomness factor (0-0.9)                 ', \
                                               default=randomness_miner, my_type='float',), 0, 0.9)
    else:
        randomness_miner = 0

    dist_hash_rate =   limit_up_down(get_input(' - Hash dist: None(0), Uniform(1), Normal(2), Poisson(3)   ', \
                                               default=dist_hash_rate, my_type='int',), 0, 3)
    if dist_hash_rate != 0 and dist_hash_rate != 3:
        randomness_hash_rate = \
                       limit_up_down(get_input('        - hash rate randomness factor (0-0.9)              ', \
                                               default=randomness_hash_rate, my_type='float',), 0, 0.9)
    else:
        randomness_hash_rate = 0
else:
    dist_miner = randomness_miner = dist_hash_rate = randomness_hash_rate = 0

do_distribution_calc = limit_up_down(get_input('Perform block distribution calc? (0=False/1=True)          ', \
                                               default=do_distribution_calc, my_type='int',), 0, 1)

# ---- Write config file
with open(config_file,"w+") as f:
    f.write(config_file_start_id + "\n")
    f.write(str(blocksToSolve) + "\n")
    f.write(str(noAlgos) + "\n")
    f.write(str(diff_algo) + "\n")
    f.write(str(targetBT) + "\n")
    f.write(str(difficulty_window) + "\n")
    f.write(str(add_randomness) + "\n")
    f.write(str(randomness_miner) + "\n")
    f.write(str(dist_miner) + "\n")
    f.write(str(randomness_hash_rate) + "\n")
    f.write(str(dist_hash_rate) + "\n")
    f.write(str(do_distribution_calc) + "\n")
    f.write(config_file_end_id)

#%% Initialize - set hash rate profiles
# ---- Profile selection
profile = [2, 1, 1, 1, 1]
c.reset()
hash_rate_profiles = []
# ---- Algo 1 hash rate profile
if profile[c.incr()] == 1:
    hash_rate_profiles.append([[[0, blocksToSolve], [1, 1]]])
elif profile[c.val()] == 2:
    hash_rate_profiles.append([[[50, 250], [2.5, 2.5]], \
                               [[250, 1800], [2.5, 1.0]], \
                               [[1800, limit_down(blocksToSolve, 1800)], [1.0, 1.0]]])
elif profile[c.val()] == 3:
    hash_rate_profiles.append([[[50, 250], [2.5, 2.5]], \
                               [[250, 1800], [2.5, 1.75]], \
                               [[1800, limit_down(blocksToSolve, 1800)], [1.0, 1.0]]])
elif profile[c.val()] == 4:
    hash_rate_profiles.append([[[1, 250], [2.0, 2.0]], \
                               [[250, 500], [1.0, 1.0]], \
                               [[500, 750], [2.0, 2.0]], \
                               [[750, 1000], [1.0, 1.0]], \
                               [[1000, 1250], [2.0, 2.0]], \
                               [[1250, 1500], [1.0, 1.0]], \
                               [[1500, 1750], [2.0, 2.0]], \
                               [[1750, limit_down(blocksToSolve, 1800)], [1.0, 1.0]]])
elif profile[c.val()] == 5:
    hash_rate_profiles.append([[[1, 250], [2.0, 2.0]], \
                               [[250, 500], [1.0, 1.0]], \
                               [[500, 750], [3.0, 3.0]], \
                               [[750, 1000], [1.0, 1.0]], \
                               [[1000, 1250], [4.0, 4.0]], \
                               [[1250, 1500], [1.0, 1.0]], \
                               [[1500, 1750], [5.0, 5.0]], \
                               [[1750, limit_down(blocksToSolve, 3000)], [1.0, 1.0]]])
elif profile[c.val()] == 6:
    hash_rate_profiles.append([[[1, 1000], [1.0, 1.5]], \
                               [[1000, 1250], [1.5, 1.5]], \
                               [[1250, 2250], [1.5, 1.0]], \
                               [[2250, limit_down(blocksToSolve, 2300)], [1.0, 1.0]]])
# ---- Algo 2 hash rate profile
if profile[c.incr()] == 1:
    hash_rate_profiles.append([[[0, blocksToSolve], [1, 1]]])
elif profile[c.val()] == 2:
    hash_rate_profiles.append([[[1, 250], [1.0, 1.0]], \
                               [[250, 500], [2.0, 2.0]], \
                               [[500, 750], [1.0, 1.0]], \
                               [[750, 1000], [2.0, 2.0]], \
                               [[1000, 1250], [1.0, 1.0]], \
                               [[1250, 1500], [2.0, 2.0]], \
                               [[1500, 1750], [1.0, 1.0]], \
                               [[1750, limit_down(blocksToSolve, 1800)], [1.0, 1.0]]])
# ---- Algo 3 hash rate profile
if profile[c.incr()] == 1:
    hash_rate_profiles.append([[[0, blocksToSolve], [1, 1]]])
elif profile[c.val()] == 2:
    hash_rate_profiles.append([[[1, 400], [1.0, 1.0]], \
                               [[400, 800], [0.5, 0.5]], \
                               [[800, 1200], [1.0, 1.0]], \
                               [[1200, 1600], [0.5, 0.5]], \
                               [[1600, 2000], [1.0, 1.0]], \
                               [[2000, limit_down(blocksToSolve, 1800)], [1.0, 1.0]]])
# ---- Algo 4 hash rate profile
if profile[c.incr()] == 1:
    hash_rate_profiles.append([[[0, blocksToSolve], [1, 1]]])
# ---- Algo 5 hash rate profile
if profile[c.incr()] == 1:
    hash_rate_profiles.append([[[0, blocksToSolve], [1, 1]]])

#%% Initialize - set mining strategies
#  hash_rate_trigger: start selfish mining when hash rate increase by this this factor
#  self_mine_factor: determines the amount of blocks to selfish mine as a factor of the difficulty_window
#  contest_tip: TODO
strategies = []
# Algo 1
smf = 15.0/difficulty_window
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=1.5, self_mine_factor=smf, contest_tip=False))
# Algo 2
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, self_mine_factor=0, contest_tip=False))
# Algo 3
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, self_mine_factor=0, contest_tip=False))
# Algo 4
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, self_mine_factor=0, contest_tip=False))
# Algo 5
strategies.append(MINE_STRATEGY(hash_rate_attack=False, hash_rate_trigger=0, self_mine_factor=0, contest_tip=False))

#%% Initialize - random function
c.reset()
print('\n')
if diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window)
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20171206(difficulty_window)
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_LWMA_01_20181127(difficulty_window)
elif diff_algo == c.incr():
    diff_algo = DIFFICULTY_TSA_20181108(difficulty_window)
else:
    diff_algo = DIFFICULTY_LWMA_00(difficulty_window)
print('\n')

#%% Initialize - blocks distribution settings
distribution = []
if do_distribution_calc == True:
    if dist_miner == 0:
        distribution_factor = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01]
    else:
        distribution_factor = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01]
else:
    distribution_factor = [0.0]

for df in distribution_factor:
    if do_distribution_calc == True:
        targetBT_profile = [1.0 - df, 1.0 + df, 1.0, 1.0, 1.0] # For distribution calc
    else:
        targetBT_profile = [1.0, 1.0, 1.0, 1.0, 1.0] # Even blocks distribution
        #targetBT_profile = [0.8, 1.2, 1.0, 1.0, 1.0] # 60/40 blocks distribution
        #targetBT_profile = [0.6, 1.4, 1.0, 1.0, 1.0] # 70/30 blocks distribution

#%% Initialize - blockchain state
#  (shared among all miners and oracle)
    state = BLOCKCHAIN_STATE(noAlgos=noAlgos, initial_difficulties=algos[_DF0], initial_block_time=1, \
                         initial_hash_rates=algos[_HR0], blockchain_target_time=targetBT, target_time_profile=targetBT_profile)
    if len(state.chain) > 0:
        state.reset(noAlgos=noAlgos, initial_difficulties=algos[_DF0], initial_block_time=1, initial_hash_rates=algos[_HR0], \
                    blockchain_target_time=targetBT, target_time_profile=targetBT_profile)

#%% Initialize - runtime
# ---- Miners
    miners = []
    for i in range(0, noAlgos):
        hash_rate = HASH_RATE(initial_hash_rate=algos[_HR0][i], profile=hash_rate_profiles[i], \
                              randomness=randomness_hash_rate, dist=get_distribution_text(dist_hash_rate), name=algos[_NAM][i])
        miners.append(MINER(randomness_miner=randomness_miner, dist=get_distribution_text(dist_miner), \
                            initial_difficulty=algos[_DF0][i], gradient=algos[_GRA][i], intercept=algos[_INT][i], \
                            name=algos[_NAM][i], algo_no=i, diff_algo=diff_algo, strategy=strategies[i], hash_rate=hash_rate, \
                            state=state))

# ---- Oracle
    oracle = ORACLE(state=state)

# ---- For debugging
    miners_vars = []
    hash_rate_vars =[]
    for i in range(0, noAlgos):
        miners_vars.append(vars(miners[i]))
        hash_rate_vars.append(vars(miners[i].hash_rate))
        oracle_vars = vars(oracle)
        state_vars = vars(state)

#%% Blockchain runtime
# ---- Initial difficulty adjustment
#  (adjusting difficulty to achieve target block time)
    settling_window = int(abs(diff_algo.difficulty_window*1.5*noAlgos))
    print('----------------------------------------------------------------------')
    print('Main: Adjusting difficulty to achieve target block time,', settling_window, 'blocks')
    print('----------------------------------------------------------------------\n')
    oracle.run(miners=miners, blocks_amount=settling_window, init=True)
    print('----------------------------------------------------------------------')
# ---- Scenario start
    print('Main: Scenario starts, solve', blocksToSolve, 'blocks')
    print('----------------------------------------------------------------------')
    oracle.run(miners=miners, blocks_amount=blocksToSolve, init=False)
    print('\n\n----------------------------------------------------------------------')
# ---- Scenario end
    print('Main: Scenario ended at block', len(oracle.state.chain), 'and time', oracle.state.system_time)
    print('----------------------------------------------------------------------')

#%% Plot results
# ---- Input hash rate profile
    fig0, axs0 = plt.subplots(1, noAlgos, figsize=(18, 5))
    fig0.subplots_adjust(hspace=0.3, wspace=0.3)
    for i in range(0, noAlgos):
        x = np.arange(1, len(miners[i].hash_rate.values) + 1)
        if noAlgos < 2:
            axs0.plot(x, miners[i].hash_rate.values)
            axs0.set_title(miners[i].name + ': Applied hash rate after init')
            axs0.grid()
            axs0.set_xlabel('block #')
        else:
            axs0[i].plot(x, miners[i].hash_rate.values)
            axs0[i].set_title(miners[i].name + ': Applied hash rate after init')
            axs0[i].set_xlabel('block #')
            axs0[i].grid()

    plt.show()

# ---- Per algo
    fig1, axs1 = plt.subplots(noAlgos, 4, figsize=(18, noAlgos*5))
    fig1.subplots_adjust(hspace=0.3, wspace=0.3)
    for i in range(0, noAlgos):
        if noAlgos < 2:
            axs1[0].plot(state.blocks[i], state.hash_rates[i], marker='.', linewidth=1)
            axs1[0].set_title(miners[i].name + ': Hash rate')
            axs1[0].grid()
            axs1[0].set_xlabel('block #')
            axs1[1].plot(state.blocks[i], state.target_difficulties[i], marker='.', linewidth=1)
            axs1[1].plot(state.blocks[i], state.achieved_difficulties[i], marker='.', linewidth=1, ls='')
            axs1[1].set_title(miners[i].name + ': Difficulty')
            axs1[1].grid()
            axs1[1].set_xlabel('block #')
            axs1[2].plot(state.blocks[i], state.solve_times[i], marker='.', linewidth=1, ls='')
            axs1[2].set_title(miners[i].name + ': Solve time')
            axs1[2].grid()
            axs1[2].set_xlabel('block #')
            axs1[3].plot(state.blocks[i], state.delta_solve_times[i], marker='.', linewidth=1, ls='')
            axs1[3].set_title(miners[i].name + ': Delta solve time')
            axs1[3].grid()
            axs1[3].set_xlabel('block #')
        else:
            axs1[i, 0].plot(state.blocks[i], state.hash_rates[i], marker='.', linewidth=1)
            axs1[i, 0].set_title(miners[i].name + ': Hash rate')
            axs1[i, 0].grid()
            axs1[i, 0].set_xlabel('block #')
            axs1[i, 1].plot(state.blocks[i], state.target_difficulties[i], marker='.', linewidth=1)
            axs1[i, 1].plot(state.blocks[i], state.achieved_difficulties[i], marker='.', linewidth=1, ls='')
            axs1[i, 1].set_title(miners[i].name + ': Difficulty')
            axs1[i, 1].grid()
            axs1[i, 1].set_xlabel('block #')
            axs1[i, 2].plot(state.blocks[i], state.solve_times[i], marker='.', linewidth=1, ls='')
            axs1[i, 2].set_title(miners[i].name + ': Solve time')
            axs1[i, 2].grid()
            axs1[i, 2].set_xlabel('block #')
            axs1[i, 3].plot(state.blocks[i], state.delta_solve_times[i], marker='.', linewidth=1, ls='')
            axs1[i, 3].set_title(miners[i].name + ': Delta solve time')
            axs1[i, 3].grid()
            axs1[i, 3].set_xlabel('block #')
    plt.show()

# ---- System values
    fig2, axs2 = plt.subplots(2, 2, figsize=(18, 10))

    y = state.get_block_times()
    x = np.arange(1, len(y) + 1)
    axs2[0, 0].plot(x, y, marker='.', ls='')
    axs2[0, 0].set_title('Blockchain: Block times (estimated)')
    axs2[0, 0].grid()
    axs2[0, 0].set_xlabel('block #')
    axs2[0, 0].text(x[round(len(y)/4)], np.min(y[settling_window:len(y)]) - 12, \
                            r'Average block time = ' + str(round(np.average(y[settling_window:len(y)]), 2)) + 's', \
                            fontsize=13, fontweight='bold')

    y = state.get_geometric_mean()
    x = np.arange(1, len(y) + 1)
    axs2[0, 1].plot(x, y)
    axs2[0, 1].set_title('Blockchain: Geometric mean of accumulated difficulties')
    axs2[0, 1].grid()
    axs2[0, 1].set_xlabel('block #')

    y = state.get_algo()
    y = [y[i]+1 for i in range(len(y))] #Add 1 to let index coresspond to name
    x = np.arange(1, len(y) + 1)
    axs2[1, 0].plot(x, y, marker='.', ls='')
    axs2[1, 0].set_title('Blockchain: Algo')
    axs2[1, 0].grid()
    axs2[1, 0].set_xlabel('block #')
    distribution.append([df, []])
    for i in range(1, noAlgos + 1):
        distribution[-1][1].append([targetBT_profile[i-1], y.count(i), round(y.count(i)/len(y)*100,1)])
        if i == noAlgos:
            y_text = i * 0.95
        else:
            y_text = i * 1.03
        axs2[1, 0].text(x[round(len(y)/7)], y_text, r'(' + miners[i-1].name + ': Target time ' + \
                        str(state.miner_target_time[i-1]) + 's (x' + str(distribution[-1][1][-1][0]) + '), ' +\
                        str(distribution[-1][1][-1][1]) + ' blocks, ' + \
                        str(distribution[-1][1][-1][2]) + '%)', fontsize=11, fontweight='bold')

    repeats = state.count_repeats()
    axs2[1, 1].plot(repeats[0], repeats[2], marker='.', ls='')
    axs2[1, 1].set_title('Blockchain: Repeats')
    axs2[1, 1].grid()
    axs2[1, 1].set_xlabel('block #')
    y_max = get_indexes_max_n_values(repeats[2], count=5)
    for i in range(0, len(y_max)):
        axs2[1, 1].text(repeats[0][y_max[i]] - repeats[0][-1]/20, \
                        repeats[2][y_max[i]] - max(repeats[2])/15, \
                            r'(' + str(miners[repeats[1][y_max[i]]].name) + ')')

    plt.show()

#%% Blocks distribution
if len(distribution) > 1:
    print('\nBlock distribution')
    print('------------------\n')
    for dist in distribution:
        print('Factor: ', dist[0])
        for i in range(0, noAlgos):
            print('  - ', miners[i].name, 'target time adjust:', dist[1][i][0], ', at', round(state.miner_target_time[i], 2) , \
                  's, ', dist[1][i][1], 'blocks, ', dist[1][i][2], '%')

    fig3, axs3 = plt.subplots(1, 1, figsize=(10, 5))
    axs3.grid()
    axs3.set_title('Block distribution')
    axs3.set_xlabel('Algo target time adjustment factor')
    axs3.set_ylabel('%')
    x = [e[0] for e in distribution]
    for i in range(0, noAlgos):
        y = [e[1][i][2] for e in distribution]
        axs3.plot(x, y, marker='*', ls='-')
    axs3.legend([n.name for n in miners])

#%% ToDo
# Implement contest_tip
# Investigate why changing the random distribution function has non-logical results

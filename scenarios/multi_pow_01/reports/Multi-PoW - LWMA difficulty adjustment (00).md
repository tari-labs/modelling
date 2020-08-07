# Multi-PoW mining simulation - LWMA difficulty adjustment (00)

(_The report must be [**viewed here**](https://demo.codimd.org/s/S1rTlu9-P) for correct rendering of the images._)

## Purpose of the report

With this simulation the performance of the LWMA difficulty adjustment in a multi-PoW scenario is investigated, with a constant hash rate profile.

**TL;DR:** _Mining algorithms in the multi-PoW setting are independent, and the LWMA difficulty adjustment algorithm copes well with stable hash rate conditions. Selecting the first block solved to extend the blockchain appears to be good strategy, and no non-linear guarding mechanisms to ensure even block distribution seems to be necessary._

## Simulation assumptions

The simulation assumptions are discussed in [**this writeup**](https://demo.codimd.org/s/SksWPUHeD), and the simulation code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01).

## Case 01: 2x algorithms, nominal values = no randomness

### Simulation parameters (Case 01):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [2]:
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]: 
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [0]: 
Perform block distribution calc? (0=False/1=True)          [0]: 
```

### Scenario timeline (Case 01):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 270 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3270 and time 385727.36 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 01):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_3251b0e815fcf6fbf56c7b27f9559b96.png)


![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_2309f4ffc96631c74de7238b27c36274.png)


### System level integrated blockchain results (Case 01):

System level block times are estimated and settles on two distinct delta block times. The moving average proves is constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_56b7a178aeeb2a6cc886448ce3a5474d.png)

## Case 02: 2x algorithms, Poisson randomness

### Simulation parameters (Case 02):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [2]: 
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]: 
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [1]:
 - Mining dist: None(0), Uniform(1), Normal(2), Poisson(3) [3]:
 - Hash dist: None(0), Uniform(1), Normal(2), Poisson(3)   [0]: 
Perform block distribution calc? (0=False/1=True)          [0]:   
```

### Scenario timeline (Case 02):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 270 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3270 and time 413535.8 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 02):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_3251b0e815fcf6fbf56c7b27f9559b96.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_eb25c3bad605536244af73406203e4db.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 02):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_c2d52d3816a5ac8266ac88e3cfb48cc4.png)

## Case 03: 3x algorithms, nominal values = no randomness

### Simulation parameters (Case 03):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]:
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]: 
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [0]:
Perform block distribution calc? (0=False/1=True)          [0]: 
```

### Scenario timeline (Case 03):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 405 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3405 and time 400743.01 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 03):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_5742366d02ea683abea8879dc9dca69e.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_aa4db2c12566241efda2f34e2b6e6649.png)

### System level integrated blockchain results (Case 03):

System level block times are estimated and settles on two distinct delta block times. The moving average proves is constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_f3d3c68a7bba11803fff7c06239219e6.png)

## Case 04: 3x algorithms, Poisson randomness

### Simulation parameters (Case 04):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]: 
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]: 
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [1]:
 - Mining dist: None(0), Uniform(1), Normal(2), Poisson(3) [3]:
 - Hash dist: None(0), Uniform(1), Normal(2), Poisson(3)   [0]: 
Perform block distribution calc? (0=False/1=True)          [0]: 
```

### Scenario timeline (Case 04):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 405 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3405 and time 427880.6 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 04):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_5742366d02ea683abea8879dc9dca69e.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ad16b8749c1ed7fa1bf61088752a2457.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 04):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_439b2c86e94aa5a565f33cecd1086195.png)

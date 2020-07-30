# Multi-PoW mining simulation - LWMA difficulty adjustment (01)

(_The report must be [**viewed here**](https://demo.codimd.org/s/HkU4-vmAU) for correct rendering of the images._)

**Edit 2020/07/22:** _Time per algo now continues from its previous time, not reset to start from new block time, thus simulating increasing probability to get a solution if it falls behind. Updated results._

## Purpose of the report

With this simulation the performance of the LWMA difficulty adjustment in a multi-PoW scenario is investigated, when introducing gradual hash rate changes.

**TL;DR:** _Mining algorithms in the multi-PoW setting are independent, and the LWMA difficulty adjustment algorithm copes well with changing hash rate conditions. Selecting the first block solved to extend the blockchain appears to be good strategy, and no non-linear guarding mechanisms to ensure even block distribution seems to be necessary._

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
Main: Scenario ended at block 3270 and time 385854.97 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 01):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_73d0ca83b9113c6f557acc29ee7b7159.png)


![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_0494e182f80317d75e491a85c9828606.png)

Notice how delta solve time settles after changes in hash rate profile.


### System level integrated blockchain results (Case 01):

System level block times are estimated and appear to be random, but the moving average proves to be fairly constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_45ae04b8f036a6bef6307168fa77227a.png)


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
Main: Scenario ended at block 3270 and time 413185.0 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 02):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_73d0ca83b9113c6f557acc29ee7b7159.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_7a4af345f12a8d417a3026c5b02d9c65.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 02):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_d9c97aea509b6028367b63fd858a1fb0.png)


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
Main: Scenario ended at block 3405 and time 400914.39 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 03):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_26e069f884522ea703956c75cca132e8.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_e4392b192ffb9aefd7f36cd4910ea59b.png)


Notice how delta solve time settles after changes in hash rate profile.

### System level integrated blockchain results (Case 03):

System level block times are estimated and appear to be random, but the moving average proves to be fairly constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_486639cadf4c20fcdfa1fd027d4e476b.png)


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
Main: Scenario ended at block 3405 and time 427448.4 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 04):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_26e069f884522ea703956c75cca132e8.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_be3a6d1c7e3db99e6027230fca499c7e.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 04):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_3708c540a478e7787ebab3b8918f3832.png)

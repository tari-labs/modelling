# Multi-PoW mining simulation - TSA difficulty adjustment

(_The report must be [**viewed here**](https://demo.codimd.org/s/r15okbz08) for correct rendering of the images._)

**Edit 2020/07/22:** _Time per algo now continues from its previous time, not reset to start from new block time, thus simulating increasing probability to get a solution if it falls behind. Updated results._

## Purpose of the report

With this simulation the performance of the TSA difficulty adjustment in a multi-PoW scenario is investigated, when introducing severe hash rate changes.

**TL;DR:** _Mining algorithms in the multi-PoW setting are independent, and the TSA difficulty adjustment algorithm copes well with severe hash rate changing conditions. Selecting the first block solved to extend the blockchain appears to be good strategy, and no non-linear guarding mechanisms to ensure even block distribution seems to be necessary._

## Simulation assumptions

The simulation assumptions are discussed in [**this writeup**](https://demo.codimd.org/s/SksWPUHeD), and the simulation code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01).


## Case 01: 2x algorithms, nominal values = no randomness

### Simulation parameters (Case 01):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [2]:
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [3]:
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
Main: Scenario ended at block 3270 and time 392158.85 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 01):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_5713803efe8426364f5c786a4e91367c.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_d7346ab65f24fbd6a7e5b572d6929528.png)

Notice how delta solve time settles after changes in hash rate profile. The drift observed in delta solve time after both algorithms' hash rate profiles have stabilized, is indicative of a slight non-linearity in the TSA algorithm feedback loop, where the target difficulty does not exactly produce the target solve time in a few decimal places.


### System level integrated blockchain results (Case 01):

System level block times are estimated and appear to be random, but the moving average proves to be fairly constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_025153891a8f2403b3dd7a774a64190f.png)

## Case 02: 2x algorithms, Poisson randomness

### Simulation parameters (Case 02):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [2]: 
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [3]: 
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
Main: Scenario ended at block 3270 and time 416156.4 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 02):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_5713803efe8426364f5c786a4e91367c.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_6cb8b371101d9572ae686e7637f05900.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 02):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_fc93a467b5417a36977079d2be7467ca.png)

## Case 03: 3x algorithms, nominal values = no randomness

### Simulation parameters (Case 03):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]:
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [3]: 
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
Main: Scenario ended at block 3405 and time 407253.33 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 03):

The independence of each algorithm can be seen below. The difference between solve time and delta solve time is evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a2dc9df9b7981d927b77bbdd97855751.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_d3b1e08d25e8e1bd8768ea0d27e07b84.png)

Notice how delta solve time settles after changes in hash rate profile. The drift observed in delta solve time after all algorithms' hash rate profiles have stabilized, is indicative of a slight non-linearity in the TSA algorithm feedback loop, where the target difficulty does not exactly produce the target solve time in a few decimal places.

### System level integrated blockchain results (Case 03):

System level block times are estimated and appear to be random, but the moving average proves to be fairly constant as expected. Block distribution to each algorithm is distributed equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a74b1b295ef7aad022be24a7fb9038fc.png)

## Case 04: 3x algorithms, Poisson randomness

### Simulation parameters (Case 04):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]: 
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [3]: 
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
Main: Scenario ended at block 3405 and time 430196.4 s
----------------------------------------------------------------------
```

### Hash rate, difficulty & solve time per algorithm (Case 04):

The randomness that was introduced shows how the difficulty algorithm will fare with with non-ideal conditions. Achieved difficulty is no longer equal to target difficulty, and the time it took to solve a block also varies.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a2dc9df9b7981d927b77bbdd97855751.png)

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_73d62b15db992dd2679534f97c6449af.png)

The difference between solve time and delta solve time is still evident, where solve time is the time it takes to get a block and the latter is a measurement of time relative to the last block added to the blockchain. The moving average of delta solve time gives an indication of that algorithm's contribution to average system block time.

### System level integrated blockchain results (Case 04):

System level block times are estimated and random, however, the moving average still proves to be fairly constant. Block distribution to each algorithm is distributed almost equal over time, and no single algorithm dominates finding consecutive blocks.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_97efb9557603a1e310ad822def72ba6b.png)

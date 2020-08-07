# Multi-PoW block distribution - (Simulation 01)

(_The report must be [**viewed here**](https://demo.codimd.org/s/Bk2gsCflD) for correct rendering of the images._)

## Purpose of the report

With this simulation an uneven block distribution for two mining algorithms is investigated.

**TL;DR:** Using 2x algorithms for multi-PoW mining with LWMA difficulty adjustment, blocks are distributed linearly and inversely proportional to the individual target block times.

## Simulation assumptions

The simulation assumptions are discussed in [**this writeup**](https://demo.codimd.org/s/SksWPUHeD), and the simulation code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01).

## Case 01: 2x algorithms, nominal values = no randomness

### Hash rate profiles used:

<p align="center"><img src="https://codimd.s3.shivering-isles.com/demo/uploads/upload_90ccf563f6ab41525a82b9274502a064.png"></p>

### Simulation parameters (Case 01):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [2]: 
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]:
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [0]: 
Perform block distribution calc? (0=False/1=True)          [1]:
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

For each data point, the individual algorithm target time was adjusted using these factors:

```
df = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01, 0.0]
algo_1_target_block_time_adjust = 1.0 + df[i]
algo_2_target_block_time_adjust = 1.0 - df[i]
```

### Effective hash rate, difficulty & solve time per algorithm (Case 01):

The simulation for target times of 336.0 s and 144.0 s for algo 1 and algo 2 respectively, corresponding to a `df = [0.40]` adjustment factor, is shown here.

![fig2](https://codimd.s3.shivering-isles.com/demo/uploads/upload_180de2a2e7ad4dfc00b56013be39858b.png)

It is noticeable that, for this nominal case, after the initial difficulty adjustment settling period, delta solve times settles on constant values. Integrated system block time shows a constant average, as shown below.

![fig3](https://codimd.s3.shivering-isles.com/demo/uploads/upload_e60dba90a74229cfdeaa8b38db7a3f73.png)

### Block distribution (Case 01):

```
Factor:  0.4
  -  Algo 1 target time adjust: 1.4 , at 336.0 s,  985 blocks,  30.1 %
  -  Algo 2 target time adjust: 0.6 , at 144.0 s,  2285 blocks,  69.9 %
Factor:  0.3
  -  Algo 1 target time adjust: 1.3 , at 312.0 s,  1147 blocks,  35.1 %
  -  Algo 2 target time adjust: 0.7 , at 168.0 s,  2123 blocks,  64.9 %
Factor:  0.2
  -  Algo 1 target time adjust: 1.2 , at 288.0 s,  1310 blocks,  40.1 %
  -  Algo 2 target time adjust: 0.8 , at 192.0 s,  1960 blocks,  59.9 %
Factor:  0.1
  -  Algo 1 target time adjust: 1.1 , at 264.0 s,  1473 blocks,  45.0 %
  -  Algo 2 target time adjust: 0.9 , at 216.0 s,  1797 blocks,  55.0 %
Factor:  0.05
  -  Algo 1 target time adjust: 1.05 , at 252.0 s,  1554 blocks,  47.5 %
  -  Algo 2 target time adjust: 0.95 , at 228.0 s,  1716 blocks,  52.5 %
Factor:  0.025
  -  Algo 1 target time adjust: 1.025 , at 246.0 s,  1595 blocks,  48.8 %
  -  Algo 2 target time adjust: 0.975 , at 234.0 s,  1675 blocks,  51.2 %
Factor:  0.01
  -  Algo 1 target time adjust: 1.01 , at 243.0 s,  1618 blocks,  49.5 %
  -  Algo 2 target time adjust: 0.99 , at 238.0 s,  1652 blocks,  50.5 %
Factor:  0.0
  -  Algo 1 target time adjust: 1.0 , at 240.0 s,  1635 blocks,  50.0 %
  -  Algo 2 target time adjust: 1.0 , at 240.0 s,  1635 blocks,  50.0 %
```

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_2a584d298884a284912dd5b54c1ceb06.png)

Blocks are distributed linearly and inversely proportional to the individual target block times.

## Case 02: 2x algorithms, Poisson randomness

### Hash rate profiles used:

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_90ccf563f6ab41525a82b9274502a064.png)

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
Perform block distribution calc? (0=False/1=True)          [1]: 
```

### Scenario timeline (Case 02):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 270 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3270 and time 413168.4 s
----------------------------------------------------------------------
```

For each data point, the individual algorithm target time was adjusted using these factors:

```
df = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01, 0.0]
algo_1_target_block_time_adjust = 1.0 + df[i]
algo_2_target_block_time_adjust = 1.0 - df[i]
```

### Effective hash rate, difficulty & solve time per algorithm (Case 02):

The simulation for target times of 336.0 s and 144.0 s for algo 1 and algo 2 respectively, corresponding to a `df = [0.40]` adjustment factor, is shown here.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_2bf4b0cbfa55325c694d2a20ce4d7576.png)

It is noticeable that, for this case with added randomness, delta solve times are random, but its average remain within a constant band. Integrated system block time shows a fairly constant average, as shown below.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ad24f227407730a4627dc7109e04aa72.png)

### Block distribution (Case 02):

```
Factor:  0.4
  -  Algo 1 target time adjust: 1.4 , at 336.0 s,  977 blocks,  29.9 %
  -  Algo 2 target time adjust: 0.6 , at 144.0 s,  2293 blocks,  70.1 %
Factor:  0.3
  -  Algo 1 target time adjust: 1.3 , at 312.0 s,  1140 blocks,  34.9 %
  -  Algo 2 target time adjust: 0.7 , at 168.0 s,  2130 blocks,  65.1 %
Factor:  0.2
  -  Algo 1 target time adjust: 1.2 , at 288.0 s,  1301 blocks,  39.8 %
  -  Algo 2 target time adjust: 0.8 , at 192.0 s,  1969 blocks,  60.2 %
Factor:  0.1
  -  Algo 1 target time adjust: 1.1 , at 264.0 s,  1465 blocks,  44.8 %
  -  Algo 2 target time adjust: 0.9 , at 216.0 s,  1805 blocks,  55.2 %
Factor:  0.05
  -  Algo 1 target time adjust: 1.05 , at 252.0 s,  1543 blocks,  47.2 %
  -  Algo 2 target time adjust: 0.95 , at 228.0 s,  1727 blocks,  52.8 %
Factor:  0.025
  -  Algo 1 target time adjust: 1.025 , at 246.0 s,  1587 blocks,  48.5 %
  -  Algo 2 target time adjust: 0.975 , at 234.0 s,  1683 blocks,  51.5 %
Factor:  0.01
  -  Algo 1 target time adjust: 1.01 , at 243.0 s,  1612 blocks,  49.3 %
  -  Algo 2 target time adjust: 0.99 , at 238.0 s,  1658 blocks,  50.7 %
Factor:  0.0
  -  Algo 1 target time adjust: 1.0 , at 240.0 s,  1626 blocks,  49.7 %
  -  Algo 2 target time adjust: 1.0 , at 240.0 s,  1644 blocks,  50.3 %
```

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_10536da262eb68b61f7761cac8a8aa30.png)

Blocks are distributed linearly and inversely proportional to the individual target block times, irrespective of the randomness introduced.

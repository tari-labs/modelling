# Multi-PoW block distribution - (Simulation 02)

(_The report must be [**viewed here**](https://demo.codimd.org/s/SyRVbYHxD) for correct rendering of the images._)

## Purpose of the report

With this simulation an uneven block distribution for three mining algorithms is investigated.

**TL;DR:** Using 3x algorithms for multi-PoW mining with LWMA difficulty adjustment, blocks are distributed linearly and inversely proportional to the individual target block times.

## Simulation assumptions

The simulation assumptions are discussed in [**this writeup**](https://demo.codimd.org/s/SksWPUHeD), and the simulation code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01).

## Case 01: 3x algorithms, nominal values = no randomness

### Hash rate profiles used:

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a5fe3f77e670150d4d407a60a0944e38.png)


### Simulation parameters (Case 01):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]:
Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)     [2]: 
Enter the system target block time (>=10)                  [120]: 
Enter the difficulty algo window (>=1)                     [90]: 
Add randomness? (0=False/1=True)                           [0]: 
Perform block distribution calc? (0=False/1=True)          [1]: 
```

### Scenario timeline (Case 01):

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 405 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3405 and time 355531.01 s
----------------------------------------------------------------------
```

For each data point, the individual algorithm target time was adjusted using these factors:

```
df = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01, 0.0]
algo_1_target_block_time_adjust = 1.0 + df[i]
algo_2_target_block_time_adjust = 1.0 - df[i]
algo_3_target_block_time_adjust = 1.0
```

### Effective hash rate, difficulty & solve time per algorithm (Case 01):

The simulation for target times of 504.0 s, 216.0 s and 360.0 s for algo 1, algo 2 and algo 3 respectively, corresponding to a `df = [0.40]` adjustment factor, is shown here.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_39f13f6453b8326bae64f3e04c544961.png)

It is noticeable that, for this nominal case, after the initial difficulty adjustment settling period, delta solve times settles on constant values. Integrated system block time shows a constant average, as shown below.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ad26e11bf1c644c8fcc3f149d0ba4a93.png)


### Block distribution (Case 01):

```
Factor:  0.4
  -  Algo 1 target time adjust: 1.4 , at 504.0 s,  723 blocks,  21.2 %
  -  Algo 2 target time adjust: 0.6 , at 216.0 s,  1674 blocks,  49.2 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1008 blocks,  29.6 %
Factor:  0.3
  -  Algo 1 target time adjust: 1.3 , at 469.0 s,  821 blocks,  24.1 %
  -  Algo 2 target time adjust: 0.7 , at 252.0 s,  1519 blocks,  44.6 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1065 blocks,  31.3 %
Factor:  0.2
  -  Algo 1 target time adjust: 1.2 , at 432.0 s,  923 blocks,  27.1 %
  -  Algo 2 target time adjust: 0.8 , at 289.0 s,  1376 blocks,  40.4 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1106 blocks,  32.5 %
Factor:  0.1
  -  Algo 1 target time adjust: 1.1 , at 397.0 s,  1024 blocks,  30.1 %
  -  Algo 2 target time adjust: 0.9 , at 324.0 s,  1253 blocks,  36.8 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1128 blocks,  33.1 %
Factor:  0.05
  -  Algo 1 target time adjust: 1.05 , at 379.0 s,  1078 blocks,  31.7 %
  -  Algo 2 target time adjust: 0.95 , at 342.0 s,  1193 blocks,  35.0 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1134 blocks,  33.3 %
Factor:  0.025
  -  Algo 1 target time adjust: 1.025 , at 369.0 s,  1107 blocks,  32.5 %
  -  Algo 2 target time adjust: 0.975 , at 351.0 s,  1164 blocks,  34.2 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1134 blocks,  33.3 %
Factor:  0.01
  -  Algo 1 target time adjust: 1.01 , at 364.0 s,  1124 blocks,  33.0 %
  -  Algo 2 target time adjust: 0.99 , at 357.0 s,  1145 blocks,  33.6 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1136 blocks,  33.4 %
Factor:  0.0
  -  Algo 1 target time adjust: 1.0 , at 360.0 s,  1135 blocks,  33.3 %
  -  Algo 2 target time adjust: 1.0 , at 360.0 s,  1135 blocks,  33.3 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1135 blocks,  33.3 %
```

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_656157dd71b7e1d44bb6cbb4269e4615.png)

Blocks are distributed linearly and inversely proportional to the individual target block times.

## Case 02: 3x algorithms, Poisson randomness

### Hash rate profiles used:

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_a5fe3f77e670150d4d407a60a0944e38.png)

### Simulation parameters (Case 02):

```
Enter number of blocks to solve after initial period       [3000]: 
Enter the number of mining algorithms (1-5)                [3]: 
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
Main: Adjusting difficulty to achieve target block time, 405 blocks
----------------------------------------------------------------------
Main: Scenario starts, solve 3000 blocks
----------------------------------------------------------------------
Main: Scenario ended at block 3405 and time 427105.2 s
----------------------------------------------------------------------
```

For each data point, the individual algorithm target time was adjusted using these factors:

```
df = [0.40, 0.30, 0.20, 0.10, 0.05, 0.025, 0.01, 0.0]
algo_1_target_block_time_adjust = 1.0 + df[i]
algo_2_target_block_time_adjust = 1.0 - df[i]
algo_3_target_block_time_adjust = 1.0
```

### Effective hash rate, difficulty & solve time per algorithm (Case 02):

The simulation for target times of 504.0 s, 216.0 s and 360.0 s for algo 1, algo 2 and algo 3 respectively, corresponding to a `df = [0.40]` adjustment factor, is shown here.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_34f97e35d4ffd37859bb1c195cf63243.png)

It is noticeable that, for this case with added randomness, delta solve times are random, but its average remain within a constant band. Integrated system block time shows a fairly constant average, as shown below.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_52dc9afa28ce6dad6dab020308aecb33.png)


### Block distribution (Case 02):

```
Factor:  0.4
  -  Algo 1 target time adjust: 1.4 , at 504.0 s,  716 blocks,  21.0 %
  -  Algo 2 target time adjust: 0.6 , at 216.0 s,  1675 blocks,  49.2 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1014 blocks,  29.8 %
Factor:  0.3
  -  Algo 1 target time adjust: 1.3 , at 469.0 s,  813 blocks,  23.9 %
  -  Algo 2 target time adjust: 0.7 , at 252.0 s,  1517 blocks,  44.6 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1075 blocks,  31.6 %
Factor:  0.2
  -  Algo 1 target time adjust: 1.2 , at 432.0 s,  916 blocks,  26.9 %
  -  Algo 2 target time adjust: 0.8 , at 289.0 s,  1375 blocks,  40.4 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1114 blocks,  32.7 %
Factor:  0.1
  -  Algo 1 target time adjust: 1.1 , at 397.0 s,  1015 blocks,  29.8 %
  -  Algo 2 target time adjust: 0.9 , at 324.0 s,  1255 blocks,  36.9 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1135 blocks,  33.3 %
Factor:  0.05
  -  Algo 1 target time adjust: 1.05 , at 379.0 s,  1068 blocks,  31.4 %
  -  Algo 2 target time adjust: 0.95 , at 342.0 s,  1195 blocks,  35.1 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1142 blocks,  33.5 %
Factor:  0.025
  -  Algo 1 target time adjust: 1.025 , at 369.0 s,  1096 blocks,  32.2 %
  -  Algo 2 target time adjust: 0.975 , at 351.0 s,  1165 blocks,  34.2 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1144 blocks,  33.6 %
Factor:  0.01
  -  Algo 1 target time adjust: 1.01 , at 364.0 s,  1113 blocks,  32.7 %
  -  Algo 2 target time adjust: 0.99 , at 357.0 s,  1146 blocks,  33.7 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1146 blocks,  33.7 %
Factor:  0.0
  -  Algo 1 target time adjust: 1.0 , at 360.0 s,  1125 blocks,  33.0 %
  -  Algo 2 target time adjust: 1.0 , at 360.0 s,  1140 blocks,  33.5 %
  -  Algo 3 target time adjust: 1.0 , at 360.0 s,  1140 blocks,  33.5 %
```

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_fcb4dd0f9a75e6c497a5315f16a13d8f.png)

Blocks are distributed linearly and inversely proportional to the individual target block times, irrespective of the randomness introduced.

# Hash Rate Attack - RandomX

(_The report must be [**viewed here**](https://demo.hedgedoc.org/s/cKgrfUlG3) for correct rendering of the images._)

## Purpose of the Report

With this simulation a RandomX hash rate attack using a step input against SHA3 miners is investigated.
Split: Algo 1 (40% SHA3) / Algo 2 (60% RandomX)


## TL;DR:

Scenario 1 - RandomX Increases 5x:

- Algo 2 (RandomX) wins these consecutive blocks in quick succession (top 4 repeats): 6 + 7 + 5 + 5 = 23

Scenario 2 - RandomX Increases 10x:

- Algo 2 (RandomX) wins these consecutive blocks in quick succession (top 4 repeats): 12 + 10 + 8 + 6 = 36

Scenario 3 - RandomX Increases 15x:

- Algo 2 (RandomX) wins these consecutive blocks in quick succession (top 4 repeats): 17 + 12 + 8 + 7 = 44


![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_f61cc56002c4ecebecdf3796f5f666c8.png)

## Simulation Assumptions

The simulation assumptions are discussed in [**this writeup**](https://demo.codimd.org/s/SksWPUHeD), and the simulation code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01).

## User Input

```
Enter number of blocks to solve after initial period       [1000]: 

Enter the number of mining algorithms (1-5)                [2]: 

Diff algo: LWMA(0), LWMA-1`17(1), LWMA-1`18(2), TSA(3)       [2]: 

Enter the system target block time (>=10)                  [120]: 

Enter the difficulty algo window (>=1)                     [90]: 

Add randomness? (0=False/1=True)                           [0]: 

Perform block distribution calc? (0=False/1=True)          [0]: 


 ----- Using difficulty algorithm: LWMA-1 version 2018-11-27 -----


 ----- Algo 1: Randomness hash_rate => none

 ----- Algo 1: Randomness miner => none

 ----- Algo 2: Randomness hash_rate => none

 ----- Algo 2: Randomness miner => none
```

## Scenario Timeline

```
----------------------------------------------------------------------
Main: Adjusting difficulty to achieve target block time, 270 blocks
----------------------------------------------------------------------
----------------------------------------------------------------------
Main: Scenario starts, solve 1000 blocks
----------------------------------------------------------------------
----------------------------------------------------------------------
Main: Scenario ended at block 1270 and time 156635.04 s
----------------------------------------------------------------------
```


## Detail Results

### Scenario 1 - RandomX Increases 5x

#### Hash Rate Profile

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_fc13fdbee7b9ff0c5928a06a066b2bce.png)

#### Algo Performance

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_c5e3e3cd0b841f7bdee3fc5a36be7fcc.png)

#### Blockchain Stats

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_f5d57996221bbc75a8ab14c6d138cfd6.png)

### Scenario 2 - RandomX Increases 10x

#### Hash Rate Profile

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_62edcee9f9dedfae18fdb34c2a844b9a.png)

#### Algo Performance

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_3ba85cdd18ce39d3aadbd87d4a49a69c.png)

#### Blockchain Stats

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_415abd5ce925c71b368f56a0201a314c.png)

### Scenario 3 - RandomX Increases 15x

#### Hash Rate Profile

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_5209f4550f9976a753076f39c469b56d.png)

#### Algo Performance

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_6843beb984f83f179627a0480f2bf5ad.png)

#### Blockchain Stats

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_ddc2f89d893614dc4ecf3d7f03df7fbc.png)

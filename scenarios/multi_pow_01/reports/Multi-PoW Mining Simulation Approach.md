# Multi-PoW Mining Simulation Approach

(_The code base is available on GitHub at [**tari-labs/modelling/scenarios/multi_pow_01**](https://github.com/tari-labs/modelling/tree/master/scenarios/multi_pow_01)_)

(_The report must be [**viewed here**](https://demo.codimd.org/s/SksWPUHeD) for correct rendering of the images._)


## General Approach

The general approach followed with this simulation is to replace the random mining process with a deterministic process. This has been done by establishing a relationship between target difficulty, available hash rate and achieved block time, which will always yield average results with a single calculation. Mining behavior that can be investigated with this approach are then based on what will happen in the average scenario. Trying to use random number generators to simulate the random mining process in the average scenario, many many iterations must be performed for each measurement, due to the law of large numbers, as explained in [this reports](https://tlu.tarilabs.com/network-analysis/probabilistic-attack/building_blocks.html#monte-carlo-simulations).


## Block Time Estimate

### Bitcoin data

Historical Bitcoin data shows a linear relationship between `block time` and `difficulty/hash rate`. This has been used as a basis to simulate the random mining process with a deterministic process.

The *Hash Rate vs Difficulty* graph shows historical hash rate estimation vs target difficulty. In the Bitcoin network, [target difficulty](https://en.bitcoin.it/wiki/Difficulty) is adjusted every 2016 blocks, approximately every two weeks. Hash rate is not directly measurable, and is estimated using relationship between measured bock time and target difficulty.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_14e1f838125422f32aed57ecfd6d0ead.png)

By dividing target difficulty with estimated hash rate, and plotting that against block time, the linear relationship is evident.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_35d207ad1f62d861ab9568695966e31b.png)

Consequently, plotting the inverse relationship yields an exponential relationship. 

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_82e07e49c2e44ded0f8c9fac4508760d.png)


### Simulation Parameters

These graphs show the linear relationship between `block time` and `difficulty/hash rate` as used in the simulations. The linear equation parameters were chosen to simulate the effect of having different mining algorithms, each with 10 times more available hash rate than the preceding algorithm, with corresponding difficulty, to produce the same block time. It is real easy to visualize that if target difficulty increases, with having a constant hash rate, block time will increase, and vice versa.

![](https://codimd.s3.shivering-isles.com/demo/uploads/upload_f47fbb0d21e5bb3de3b137fbf4a48991.png)


## Mining

To simulate what will happen in a real life scenario, using multiple mining algorithms, an oracle is used to select the first available block to add it to the blockchain, and then share the blockchain state with all mining algorithms.

The oracle asks each participating mining algorithm to produce the next block. Each mining algorithm runs independently, without any inter-dependencies, using its own difficulty adjustment. Mining is based on the average time it takes to solve a block for a given hash rate and target difficulty (see _**Block Time Estimate**_).

```
solve_time = (target_difficulty/hash_rate) * gradient_r + self.intercept
achieved_difficulty = ((solve_time - self.intercept) / self.gradient) * hash_rate

```

If a mining algorithm did not produce the previous solution, a small time overhead can be added to its next target solve time, of say 1% of target block time, to simulate the inefficiencies of block propagation delay on the network, in order to have a new block to solve. (_See discussion about new block propagation time [in this article](https://medium.facilelogin.com/the-mystery-behind-block-time-63351e35603a). It quotes a figure of ~12.6 s to reach 95% of the nodes using the old Bitcoin Relay Network, as published [in this 2013 paper](https://tik-db.ee.ethz.ch/file/49318d3f56c1d525aabf7fda78b23fc0/P2P2013_041.pdf). With the new [FIBRE network](https://bitcoinrelaynetwork.org/stats.html) this time has come down to ~0.633 s for 95% nodes to receive the new block at tier 4._)

```
if self.algo_no != self.state.chain[-1].algo:
    solve_time = solve_time + self.new_block_overhead_time
```

Each mining algorithm returns its actual solve time as well as the delta solve time based on the current time, so that the oracle can select the first available block. If a mining algorithm produced the previous solution, the time lag will be zero.

```
lag = time_now - previous_time_stamp
delta_time = solve_time - lag
```

The mining algorithm that returns with the fastest `delta_time` is chosen, except when one or more blocks are presented for reorg, in which case the oracle will select the best chain based on a geometric mean calculation. This has the effect that, with stable conditions, average block times (BT) will be smooth, but actual block times will be fluctuating.

```
            (time_now)  Y
Algo 1:     --------1--------1--------1--------1--------1--------1--------1--------
                    |   T1   |
                        |dT1 |
Algo 2:     ----------2----------2----------2----------2----------2----------2-----
                      |   T2     |
                        |  dT2   |
Algo 3:     ------------3------------3------------3------------3------------3------
                        |    T3      |
                        |    dT3     |
Actual BT:  ========1=2=3====1===2===31=====2==1==3====21======3=12=======1=32=====
Average BT: =^===^===^===^===^===^===^===^===^===^===^===^===^===^===^===^===^===^=
```


## Randomness

Randomness can be added to the hash rate profile and/or mining calculation, to simulate real world conditions that will not always yield smooth and average results.

```
Inputs: target_difficulty, hash_rate, time_now, previous_time_stamp

#Apply randomess to hash rate
hash_rate = self.rand1.get_value(hash_rate)
#Randomness can influence the achieved difficulty
gradient_r = self.rand2.get_value(self.gradient)
solve_time = (target_difficulty/hash_rate) * gradient_r + self.intercept
achieved_difficulty = ((solve_time - self.intercept) / self.gradient) * hash_rate
#Randomness can influence the solve time
solve_time = self.rand2.get_value(solve_time)

```

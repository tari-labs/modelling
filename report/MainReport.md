# Probabilistic Attack Vector

- [Introduction](#introduction)
	- [Aim](#aim)
	- [The Tari Digital Assets Network](#the-tari-digital-assets-network)  
- [Literature Review](#literature review)
	- [Types of Distribution](#types-of-distribution)
		- [Hypergeometric Distribution](#hypergeometric-distribution)
		- [Binomial Distribution](#binomial-distribution)
- [Methodology](#methodology)
	- [Notation Used](#notation-used)
	- [Formulae](#formulae)
		- [Hypergeometric Distribution](#hypergeometric-distribution)
		- [Binomial Distribution](#binomial distribution)
		- [Summation](#summation)
	- [Explanation of hypergeometric distribution ](#combinations)
	- [The Use of Python](#the-use-of-python)
- [Results](#results)
	- [Plots](#plots) 
	- [Demonstration](#demonstration)
- [Discussion](#discussion) 
- [Conclusion and Recommendations](#conclusions-and-recommendations)
- [References](#references)
- [Contributions](#contributors) 

## Introduction
(What you researched and why)

### Aim 
This research aims to provide answers to questions about the Tari DAN environment: Probabilistic ttack vector with regards to the total nodes, compromised nodes, committee size and BFT threshold.

### The Tari Digital Assets Network 
Digital assets (DAs) are managed by committees of special nodes, Validator nodes . 

Validator nodes form committees to manage the digital assets, their state change and ensures that the rules governing asset contracts are enforced. 

Where was the idea borne from? 

There would be a pool with *N* nodes, the pool contains *m* malicious nodes or bad actors,  within the pool a random selection of nodes are drawn *n*, from that selection the probablity of drawning a threshold of bad actors *T* needs to be calculated.  

## Literature Review 
(Other relevant research in this area)

### Types of Distribution 

When considering solving the probability of the of an attacker controlling the majority of nodes in the network, the various types of probability distributions need to be analysed with regards to the specific circumstances and variables of the problem. Types of probability distribution can be split into finite and infinite support [[1]]; where support is defined as a real-valued function *f*, which is the subset of the domain containing those elemets which are not mapped to zero. If the domain of *f* is a topological space, teh support of *f* is instead defined as the smallest closed set containing all points not mapped to zero. [[2]] 

#### Hypergeometric Distribution:

Hypergeometric distribution is a dicrete probability distribution that describes the probability *k* successes (random draws for which the object drawn has a specified feature) in *n* draws, *without* replacement, from a finite population of  size *N* that contains exactly *K* objects with that feature, wherein each draw is either a success or a failure. [[3]]

Selecting nodes without replacement, i.e. selecting all 6 nodes at once

#### Binomial Distribution:

The binomial distribution with parameters Selecting nodes with replacement, i.e. selecting each node, noting whether it is malicious or friendly and returning back to the committee. [[4]]

## Methodolgy 
(What you did and how you found it)

### Notation Used  

This section conmtains the general notation of statistical expressions when specifically referenced. This information serves as important pre-knolwedge for the remainder of the report. 

- Let $N$ be the total number of nodes in the network 
- Let $n$ be the committee size
- Let $m$ be the number of bad actors 
- Let $T$ be the BFT threshold (at least two thirds, however in this case it may vary) 

### Formulae

#### Hypergeometric Distribution 

$$
P=\frac{mCT . (N-m)C(n-T)}{NCn}
$$

#### Binomial Distribution  

$$
P=nCT.\biggl(\frac{m}{n}\biggr)^{T}.\biggl(\frac{N-m}{n}\biggr)^{n-T}
$$

#### Summation 

$$
P_{tot} = \sum_{i=T}^{n} P(N,m,n,i)
$$

### Explanation of hypergeometric distribution (combinations)

### The Use of Python 

## Results 
(What you found)

### Plots 

### Demonstration 

## Discussion 
(Relevance of your results, how it fits with other research in the area)

## Conclusion and Recommendations
(Summary of results/findings and what needs to be done as a reuslt of your findings)

## References

[[1]] B. W. Contributors, “List of probability distributions”, 2019. Available: <https://en.wikipedia.org/wiki/List_of_probability_distributions>. 
Date accessed: 2019-05-13. 

[1]: https://en.wikipedia.org/wiki/List_of_probability_distributions
"List of probability distributions"

[[2]] B. W. Contributors, “Support (mathematics)”, 2019. Available: <https://en.wikipedia.org/wiki/Support_(mathematics)>. 
Date accessed: 2019-05-13. 

[2]: https://en.wikipedia.org/wiki/Support_(mathematics)
“Support (mathematics)”

[[3]] B. W. Contributors, “Hypergeometric distribution”, 2019. Available: <https://en.wikipedia.org/wiki/Hypergeometric_distribution>. 
Date accessed: 2019-05-13. 

[3]: https://en.wikipedia.org/wiki/Hypergeometric_distribution
"Hypergeometric distribution"

[[4]] B. W. Contributors, “Binomial distribution", 2019. Available: <https://en.wikipedia.org/wiki/Binomial_distribution>. 
Date accessed: 2019-05-13. 

[4]: https://en.wikipedia.org/wiki/Binomial_distribution
“Binomial distribution"

##Contributions

- <https://github.com/kevoulee>
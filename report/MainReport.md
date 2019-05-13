# Probability of Attack Model 

- - [Introduction](#introduction)
		- Types of Distribution (#types-of-distribution)
			- Hypergeometric Distribution (#hypergeometric-distribution)
			- Binomial Distribution (#binomial-distribution)
	- [Conclusion, Observations and Recommendations](#conclusions-observations-and-recommendations)
	- [References](#references)
	- [Contributions](#contributors) 

## Introduction

The question that was posed is what is the probability of an attacker controlling the majority of nodes in the network? 

### Types of Distribution 

When considering solving the probability of the of an attacker controlling the majority of nodes in the network, the various types of probability distributions need to be analysed with regards to the specific circumstances and variables of the problem. Types of probability distribution can be split into finite and infinite support [[1]]; where support is defined as a real-valued function *f*, which is the subset of the domain containing those elemets which are not mapped to zero. If the domain of *f* is a topological space, teh support of *f* is instead defined as the smallest closed set containing all points not mapped to zero. [[2]] 

#### Hypergeometric Distribution:

Hypergeometric distribution is a dicrete probability distribution that describes the probability *k* successes (random draws for which the object drawn has a specified feature) in *n* draws, *without* replacement, from a finite population of  size *N* that contains exactly *K* objects with that feature, wherein each draw is either a success or a failure. [[3]]

Selecting nodes without replacement, i.e. selecting all 6 nodes at once

#### Binomial Distribution:

The binomial distribution with parameters Selecting nodes with replacement, i.e. selecting each node, noting whether it is malicious or friendly and returning back to the committee. [[4]]

### Variables 

- Let $N$ be the total number of nodes in the network 
- Let $n$ be the committee size
- Let $m$ be the number of bad actors 
- Let $T$ be the BFT threshold (at least two thirds, however in this case it may vary) 

### Formulae

##### Hypergeometric Distribution 

$$
P=\frac{mCT . (N-m)C(n-T)}{NCn}
$$

##### Binomial Distribution  

$$
P=nCT.\biggl(\frac{m}{n}\biggr)^{T}.\biggl(\frac{N-m}{n}\biggr)^{n-T}
$$

##### Summation 

$$
P_{tot} = \sum_{i=T}^{n} P(N,m,n,i)
$$

### Explanation of hypergeometric distribution (combinations)

### Simple plot with verification 

### Demonstration 

## Conclusion, Observations and Recommendations


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
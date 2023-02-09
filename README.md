# stochastic_processes
Python programs for solving Markov Chain and Martingale Problems

## Solving Irreducible Markov Chains for the Stationary Distribution

First, edit stat_dist.py to use the desired matrix, then run the following command
```
python stat_dist.py
```

Output = π, where π(x) is the long term proportion of time spent in state x

## Solving Reducible Markov Chains for Hitting Probabilities and Transient State Visits

**note: the order of transient states WILL change, but their relative order will not change

First, edit reducible.py to use the desired matrix, then run the following command

```
python reducible.py
```

Output = the recurrent classes and transient states found, the expected number of visits to transient state j starting at transient state i (the (i,j) entry into the visits matrix), and the probability of hitting recurrent class j starting at transient state i (the (i,j) entry into the hitting probabilities matrix.

Example Output: 
```
recurrent classes: [[0], [11]]
transient states: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
visits:
 [[1.00097752 0.50048876 0.00391007 0.25024438 0.06256109 0.00195503
  0.00782014 0.12512219 0.01564027 0.03128055]
 [0.00195503 1.00097752 0.00782014 0.50048876 0.12512219 0.00391007
  0.01564027 0.25024438 0.03128055 0.06256109]
 [0.25024438 0.12512219 1.00097752 0.06256109 0.01564027 0.50048876
  0.00195503 0.03128055 0.00391007 0.00782014]
 [0.00391007 0.00195503 0.01564027 1.00097752 0.25024438 0.00782014
  0.03128055 0.50048876 0.06256109 0.12512219]
 [0.01564027 0.00782014 0.06256109 0.00391007 1.00097752 0.03128055
  0.12512219 0.00195503 0.25024438 0.50048876]
 [0.50048876 0.25024438 0.00195503 0.12512219 0.03128055 1.00097752
  0.00391007 0.06256109 0.00782014 0.01564027]
 [0.12512219 0.06256109 0.50048876 0.03128055 0.00782014 0.25024438
  1.00097752 0.01564027 0.00195503 0.00391007]
 [0.00782014 0.00391007 0.03128055 0.00195503 0.50048876 0.01564027
  0.06256109 1.00097752 0.12512219 0.25024438]
 [0.06256109 0.03128055 0.25024438 0.01564027 0.00391007 0.12512219
  0.50048876 0.00782014 1.00097752 0.00195503]
 [0.03128055 0.01564027 0.12512219 0.00782014 0.00195503 0.06256109
  0.25024438 0.00391007 0.50048876 1.00097752]]
hitting probabilities:
 [[0.90909091 0.09090909]
 [0.81818182 0.18181818]
 [0.72727273 0.27272727]
 [0.63636364 0.36363636]
 [0.54545455 0.45454545]
 [0.45454545 0.54545455]
 [0.36363636 0.63636364]
 [0.27272727 0.72727273]
 [0.18181818 0.81818182]
 [0.09090909 0.90909091]]
Nate's probability of winning is 0.909091
Nate's probability of losing is 0.090909
Nate's expected winnings is -0.000000
Justin's probability of winning is 0.090909
Justin's probability of losing is 0.909091
Justin's expected winnings is -0.000000
```

# stochastic_processes

Python programs for solving Markov Chain problems.

## Solving Irreducible Markov Chain for the Stationary Distribution

This algorithm finds the eigenvalue = 1 of the matrix, and then finds the eigenvector corresponding to that eigenvalue. The eigenvector, normalized to sum to 1, is the stationary distribution of the Markov Chain.

First, edit stat_dist.py to use the desired matrix, then run the following command:

```
python stat_dist.py
```

Output = π, where π(x) is the long term proportion of time spent in state x

## Solving Reducible Markov Chain for Hitting Probabilities and Transient State Visits

This algorithm first uses Kosaraju's algorithm to find the strongly connected components of the graph. Then it uses a depth-first algorithm I came up with to distinguish the recurrent classes from transient states among the strongly connected components. From the original matrix, the algorithm derives matrices S and Q, where M = (1-Q)^-1 = the expected number of visits to each transient state conditioned on starting state, and M*S = the hitting probabilities conditioned on starting state.

**note: the indexes of the states WILL change, but their relative order will not change

First, edit reducible.py to use the desired matrix, then run the following command:

```
python reducible.py
```

Output = the recurrent classes and transient states found, the expected number of visits to transient state j starting at transient state i (the (i,j) entry into the visits matrix), and the probability of hitting recurrent class j starting at transient state i (the (i,j) entry into the hitting probabilities matrix.

### Example Usage

The origin of this example comes from a bet I made with my roommate. After playing poker, I had $20 in my pot and my roommate had $2, and we decided to go all-in repeatedly until one of us won the other's money. I was shocked to lose the bet, so I wanted to find out what the odds were of me winning. I decided to model the problem as a Markov Chain, where the states are the amount of money I have, and the transitions are the amount of money I win or lose in each round. I then used the reducible.py program to find the hitting probabilities, and thus, the probability of winning and expected value of the bet, which was 10/11 and $0, respectively.

Input:

```python
indices = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
mat = [
    # [0, 2, 4, 6, 8, 10,12,14,16,18,20,22]
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
    [.5, 0, .5, 0, 0, 0, 0, 0, 0, 0, 0, 0],\
    [.5, 0, 0, 0, .5, 0, 0, 0, 0, 0, 0, 0],\
    [.5, 0, 0, 0, 0, 0, .5, 0, 0, 0, 0, 0],\
    [.5, 0, 0, 0, 0, 0, 0, 0, .5, 0, 0, 0],\
    [.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, .5, 0],\
    [0, .5, 0, 0, 0, 0, 0, 0, 0, 0, 0, .5],\
    [0, 0, 0, .5, 0, 0, 0, 0, 0, 0, 0, .5],\
    [0, 0, 0, 0, 0, .5, 0, 0, 0, 0, 0, .5],\
    [0, 0, 0, 0, 0, 0, 0, .5, 0, 0, 0, .5],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, .5, 0, .5],\
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
]
```

Output:

```

recurrent classes: [[0], [22]]
transient states: [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
S:
 [[0.5 0. ]
 [0.5 0. ]
 [0.5 0. ]
 [0.5 0. ]
 [0.5 0. ]
 [0.  0.5]
 [0.  0.5]
 [0.  0.5]
 [0.  0.5]
 [0.  0.5]]
Q:
 [[0.  0.5 0.  0.  0.  0.  0.  0.  0.  0. ]
 [0.  0.  0.  0.5 0.  0.  0.  0.  0.  0. ]
 [0.  0.  0.  0.  0.  0.5 0.  0.  0.  0. ]
 [0.  0.  0.  0.  0.  0.  0.  0.5 0.  0. ]
 [0.  0.  0.  0.  0.  0.  0.  0.  0.  0.5]
 [0.5 0.  0.  0.  0.  0.  0.  0.  0.  0. ]
 [0.  0.  0.5 0.  0.  0.  0.  0.  0.  0. ]
 [0.  0.  0.  0.  0.5 0.  0.  0.  0.  0. ]
 [0.  0.  0.  0.  0.  0.  0.5 0.  0.  0. ]
 [0.  0.  0.  0.  0.  0.  0.  0.  0.5 0. ]]
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
Nate's expected winnings is 0.000000
Justin's probability of winning is 0.090909
Justin's probability of losing is 0.909091
Justin's expected winnings is 0.000000
```

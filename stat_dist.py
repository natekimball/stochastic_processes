import numpy as np
from scipy.linalg import eig
from fractions import Fraction as frac
from reducible import scc

transition_mat = [
    [.5, .5],
    [.3, .7]
]

# Algorithm 1: Finding the period d of transition_mat
# 1. From an arbitrary root node, perform a breadth-first
# search of G producing the rooted tree T.
# 2. The period g is given by gcd{val(e) > 0 : e ∈ T}
# implement algorithm 1

def periodicity(mat):
    val, parent = levels(mat)
    # return np.gcd.reduce([x for x in val if x > 0])
    other_vals = []
    for j in len(mat):
        for i in len(mat):
            if mat[i,j] > 0 and i!=j and parent[j] != i:
                # edges.append((i,j))
                other_vals.append(val[j] - val[i] if val[j] > val[i] else val[i] - val[j])
    return np.gcd.reduce(other_vals)  

def levels(mat):
    val = [0 for _ in mat]
    parent = [-1 for _ in mat]
    queue = [0]
    while queue:
        u = queue.pop(0)
        for v in range(len(mat)):
            if mat[u,v] > 0 and parent[v] == -1:
                parent[v] = u
                val[v] = val[u] + 1
                queue.append(v)
    return val, parent    

classes = scc(transition_mat)
if len(classes) > 1:
    print("reducible matrix does not have a stationary distribution")
    exit()
period = periodicity(transition_mat)
if period > 1:
    print("Markov Chain has periodicity of %d" % period)
else:
    print("Markov Chain is aperiodic, so it has a limiting distribution")

S, U = eig(np.matrix(transition_mat).T)
stationary = np.array(U[:,np.isclose(S,1)].flat)
stationary = stationary / np.sum(stationary)
stationary = [str(frac(x).limit_denominator()) for x in stationary]
print(stationary)
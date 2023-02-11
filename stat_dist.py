import numpy as np
from scipy.linalg import eig
from fractions import Fraction as frac
from reducible import scc
import math

transition_mat = [
    [.5, .5],
    [.3, .7]
]

def periodicity(P):
    n = P.shape[0]
    for i in range(1, n+1):
        Pi = np.linalg.matrix_power(P, i)
        rank = np.linalg.matrix_rank(Pi)
        if rank == n:
            return i
    return 1

def periodicity_maybe(mat):
    val, parent = levels(mat)
    other_vals = []
    for j in range(len(mat)):
        for i in range(len(mat)):
            if mat[i,j] > 0 and i!=j and parent[j] != i:
                other_vals.append(val[j] - val[i] +1 if val[j] > val[i] else val[i] - val[j] + 1)
    # print(other_vals)
    return gdc(other_vals) if other_vals else 1

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

def gdc(vals):
    gcd = vals[0]
    for i in range(1, len(vals)):
        gcd = math.gcd(gcd, vals[i])
    return gcd

transition_mat = np.array(transition_mat)
classes = scc(transition_mat)
if len(classes) > 1:
    print("reducible matrix does not have a stationary distribution")
    exit()

period = periodicity(transition_mat)
if period > 1:
    print("Markov Chain has periodicity of %d" % period)
else:
    print("Markov Chain is aperiodic, so it has a limiting distribution")

S, U = eig(transition_mat.T)
stationary = np.array(U[:,np.isclose(S,1)].flat)
stationary = stationary / np.sum(stationary)
stationary = [str(frac(x).limit_denominator()) for x in stationary]
print(stationary)
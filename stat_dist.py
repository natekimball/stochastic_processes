import numpy as np
from scipy.linalg import eig
from fractions import Fraction as frac
import util
import math

transition_mat = [
    [3/4, 1/4, 0, 0, 0, 0, 0],
    [1/2, 1/4, 1/4, 0, 0, 0, 0],
    [1/4, 1/4, 1/4, 1/4, 0, 0, 0],
    [1/4, 0, 1/4, 1/4, 1/4, 0, 0],
    [1/4, 0, 0, 1/4, 1/4, 1/4, 0],
    [1/4, 0, 0, 0, 1/4, 1/4, 1/4],
    [1/4, 0, 0, 0, 0, 1/4, 1/2]
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
            if mat[i,j] > 0 and parent[j] != i:
                other_vals.append(val[j] - val[i] +1 if val[j] > val[i] else val[i] - val[j] + 1)
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

def stationary_dist(transition_mat):
    S, U = eig(transition_mat.T)
    stationary = np.array(U[:,np.isclose(S,1)].flat)
    return (stationary / np.sum(stationary)).real

def solve_irreducible(transition_mat):
    transition_mat = np.array(transition_mat)
    if len(util.scc(transition_mat)) > 1:
        print("reducible matrix does not have a unique stationary distribution")
        exit()
    print("Markov Chain is irreducible, so it has a unique stationary distribution")
    
    period = periodicity(transition_mat)
    if period > 1:
        print("Markov Chain has periodicity of %d" % period)
        print("maybe: %d" % periodicity_maybe(transition_mat))
    else:
        print("Markov Chain is aperiodic, so it has a limiting distribution")
        
    π = stationary_dist(transition_mat)
    print("π: %s" % util.format_array(π))
    
if __name__ == "__main__":
    solve_irreducible(transition_mat)
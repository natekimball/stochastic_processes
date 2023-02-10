import numpy as np
from scipy.linalg import eig
from fractions import Fraction as frac
from reducible import scc

transition_mat = np.matrix([
    [.5, .5],
    [.3, .7]
])

if len(scc(transition_mat)) > 1:
    # won't work
    print("reducible matrix does not have a stationary distribution")
    exit()

# Algorithm 1: Finding the period d of transition_mat
# 1. From an arbitrary root node, perform a breadth-first
# search of G producing the rooted tree T.
# 2. The period g is given by gcd{val(e) > 0 : e ∈ T}
# implement algorithm 1

def bfs(mat):
    visited = [False for _ in range(len(mat))]
    val = []
    queue = [(0,0)]
    visited[0] = True
    while queue:
        i,v = queue.pop(0)
        for j in range(len(mat)):
            if mat[i][j] != 0:
                # if visited[j]:
                #     val.append(v+1)
                if not visited[j]:
                    queue.append((j,v+1))
                    visited[j] = True

S, U = eig(transition_mat.T)
stationary = np.array(U[:,np.isclose(S,1)].flat)
stationary = stationary / np.sum(stationary)
stationary = [str(frac(x).limit_denominator()) for x in stationary]
print(stationary)
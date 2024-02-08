import numpy as np
from scipy.linalg import eig
import util
import math

# transition_mat = [
#     [3/4, 1/4, 0, 0, 0, 0, 0],
#     [1/2, 1/4, 1/4, 0, 0, 0, 0],
#     [1/4, 1/4, 1/4, 1/4, 0, 0, 0],
#     [1/4, 0, 1/4, 1/4, 1/4, 0, 0],
#     [1/4, 0, 0, 1/4, 1/4, 1/4, 0],
#     [1/4, 0, 0, 0, 1/4, 1/4, 1/4],
#     [1/4, 0, 0, 0, 0, 1/4, 1/2]
# ]

transition_mat = [
    [0,1,0],
    [0,0,1],
    [1,0,0]
    # [0,.5,.5],
    # [1,0,0],
    # [1,0,0]
]

def find_period(mat):
    val, parent = levels(mat)
    other_vals = []
    for j in range(len(mat)):
        for i in range(len(mat)):
            if mat[i,j] > 0 and parent[j] != i:
                other_vals.append(val[j] - val[i] +1 if val[j] > val[i] else val[i] - val[j] + 1)
    return gcd(other_vals) if other_vals else 1

# def find_period(markov_chain):
#     n = len(markov_chain)
#     periods = []
#     for i in range(n):
#         # Find all paths from state i back to itself
#         paths = [[i]]
#         while True:
#             new_paths = []
#             for path in paths:
#                 for j in range(n):
#                     if markov_chain[path[-1]][j] > 0:
#                         if j == i:
#                             # Found a path back to i
#                             periods.append(len(path))
#                         else:
#                             # Extend the path to j
#                             new_paths.append(path + [j])
#             if not new_paths:
#                 break
#             paths = new_paths

    # Find the GCD of all periods
    # period_gcd = gcd(periods)

    # if period_gcd > 1:
    #     print("Markov chain is periodic with period", period_gcd)
    # else:
    #     print("Markov chain is aperiodic")


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

def gcd(vals):
    gcd = vals[0]
    for i in range(1, len(vals)):
        gcd = math.gcd(gcd, vals[i])
    return gcd

def stationary_dist(P):
    S, U = eig(P.T)
    stationary = np.array(U[:,np.isclose(S,1)].flat)
    return (stationary / np.sum(stationary)).real

def solve_irreducible(P, indices=None):
    if len(util.scc(P)) > 1:
        print("reducible matrix does not have a unique stationary distribution")
        exit()
    print("Markov Chain is irreducible, so it has a unique stationary distribution")

    indices = list(range(len(P))) if not indices else indices
    print("indices: %s" % indices)
    π = stationary_dist(P)
    print("π: %s" % util.format_array(π))
    print("E[T\u2096]: %s" % util.format_array(1/π))
    assert np.isclose(np.sum(π), 1)
    
    # period = find_period(P)
    # if period > 1:
    #     print("Markov Chain might have a period of %d" % period)
    # else:
    #     print("Markov Chain might be aperiodic, so it has a limiting distribution")
    power = np.linalg.matrix_power(P,20)
    if np.allclose(power, power@P):
        print("Markov Chain is likely aperiodic, so it has a limiting distribution")
    else:
        power = np.linalg.matrix_power(P,40)
        if np.allclose(power, power@P):
            print("Markov Chain is likely aperiodic, so it has a limiting distribution")
        else:
            print("Markov Chain is likely not aperiodic")
    print("verify periodicity, regardless")
    
if __name__ == "__main__":
    solve_irreducible(np.array(transition_mat))
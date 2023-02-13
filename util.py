from fractions import Fraction as frac
import numpy as np
from reducible import solve_reducible
from stat_dist import solve_irreducible

def solve(P, indices=None, recurrent_classes=None):
    if recurrent_classes or len(scc(P)) > 1:
        solve_reducible(P, indices, recurrent_classes)
    else:
        solve_irreducible(P, indices)

def dfs(P, i, visited, order):
    visited[i] = True
    for j in range(len(P)):
        if P[i,j] != 0 and not visited[j]:
            dfs(P, j, visited, order)
    order.insert(0,i)

def scc(P):
    visited = [False for _ in range(len(P))]
    order = []
    for i in range(len(P)):
        if not visited[i]:
            dfs(P, i, visited, order)
    classes = []
    visited = [False for _ in range(len(P))]
    while order:
        i = order.pop()
        if not visited[i]:
            cl = []
            dfs(P, i, visited, cl)
            classes.append(cl)
    return classes

def format(dec):
    fraction = frac(str(dec)).limit_denominator()
    numerator = fraction.numerator
    denominator = fraction.denominator
    if numerator == 0:
        return "0"
    if denominator == 1:
        return str(numerator)
    if denominator == 0:
        return "NaN"
    return str(numerator) + "/" + str(denominator)

def format_matrix(M):
    return '['+'\n'.join(['['+', '.join([format(x) for x in row])+']' for row in M])+']'

def format_array(A):
    return '['+', '.join([format(x) for x in A])+']'
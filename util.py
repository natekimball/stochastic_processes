from fractions import Fraction as frac
import numpy as np
from reducible import solve_reducible
from stat_dist import solve_irreducible

def solve(P, indices=None, recurrent_classes=None):
    P = np.array(P)
    assert np.allclose(np.sum(P, axis=1), np.ones(P.shape[0])), "P is not a valid stochastic matrix"
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

def transient(indices, recurrent_classes):
    return [r for i,r in enumerate(indices) if find_class(i, recurrent_classes) == -1]

def find_class(j, classes):
    for i,c in enumerate(classes): 
        if j in c:
            return i
    return -1

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

def print_lin_system(A):
    for i in range(len(A)):
        s=""
        first = True
        for j in range(len(A)-2):
            if A[i,j]:
                a = A[i,j]
                sign = ("- " if not first else "-") if a<0 else ("" if first else "+ ")
                first = False
                if int(a) == a:
                    a = int(a)
                    if abs(a) == 1:
                        s += sign + f"π_{j+1} "
                        continue
                a = abs(a)
                s += sign + f"{a}*π_{j+1} "
        if int(A[i,-2]) == A[i,-2]:
            a2 = int(A[i,-2])
        if int(A[i,-1]) == A[i,-1]:
            a1 = int(A[i,-1])
        if a2:    
            if abs(a2) == 1:
                s += signum(a2) + f" π_{len(A)-1} = {a1}"
            else:
                s += signum(a2) + f" {abs(a2)}*π_{len(A)-1} = {a1}"
        else:
            s += f"= {a1}"
        print(s)

def signum(x):
    return "+" if x>=0 else "-"
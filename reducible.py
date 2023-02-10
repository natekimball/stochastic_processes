import numpy as np
from scipy.linalg import eig 
from fractions import Fraction as frac

def dfs(mat, i, visited, order):
    visited[i] = True
    for j in range(len(mat)):
        if mat[i][j] != 0 and not visited[j]:
            dfs(mat, j, visited, order)
    order.insert(0,i)

def scc(mat):
    visited = [False for _ in range(len(mat))]
    order = []
    for i in range(len(mat)):
        if not visited[i]:
            dfs(mat, i, visited, order)
    classes = []
    visited = [False for _ in range(len(mat))]
    while order:
        i = order.pop()
        if not visited[i]:
            cl = []
            dfs(mat, i, visited, cl)
            classes.append(cl)
    return classes[:-1]

def transient(indices, recurrent_classes):
    new = []
    for i,r in enumerate(indices):
        if find_class(i, recurrent_classes) == -1:
            new.append(r)
    return new

def find_class(j, classes):
    for i,c in enumerate(classes): 
        if j in c:
            return i
    return -1

def get_S_and_Q(mat, classes):
    r = len(classes)
    S = [[0 for _ in range(r)] for _ in range(len(mat)-r)]
    Q = [[0 for _ in range(len(mat[0])-r)] for _ in range(len(mat)-r)]
    rs = []
    for c in classes:
        for a in c:
            rs.append(a)
            
    q = 0
    for i,row in enumerate(mat):
        if i in rs:
            q+=1
            continue
        s = 0
        for j,el in enumerate(row):
            if j in rs:
                j = find_class(j, classes)
                for k in classes[j]:
                    S[i-q][j] += mat[i][k]
                s += 1
            else:
                Q[i-q][j-s] = mat[i][j]
    return np.matrix(S), np.matrix(Q)

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

recurrent_classes = scc(mat)
transient_states = transient(indices, recurrent_classes)
S,Q = get_S_and_Q(mat, recurrent_classes)
M = np.linalg.inv(np.identity(len(Q))-Q)
hitting_probabilities = M*S
print("recurrent classes:", [[indices[i] for i in c] for c in recurrent_classes])
print("transient states:", transient_states)
print("visits:\n",M)
print("hitting probabilities:\n",hitting_probabilities)
# print([[frac(str(x)) for x in y] for y in hitting_probabilities])
print("Nate's probability of winning is %f" % hitting_probabilities[-1,1])
print("Nate's probability of losing is %f" % hitting_probabilities[-1,0])
print("Nate's expected winnings is %f" % round(hitting_probabilities[-1,1]*2 - hitting_probabilities[-1,0]*20))
print("Justin's probability of winning is %f" % hitting_probabilities[0,1])
print("Justin's probability of losing is %f" % hitting_probabilities[0,0])
print("Justin's expected winnings is %f" % round(hitting_probabilities[0,1]*20 - hitting_probabilities[0,0]*2))


# for if recurrence_classes are all are single states
def get_S_and_Q_single_classes(mat, recurrence_classes):
    r = len(recurrence_classes)
    new_mat = np.matrix([[0 for _ in mat[0]] for _ in mat])
    S = [[0 for _ in range(r)] for _ in range(len(mat)-r)]
    Q = [[0 for _ in range(len(mat[0])-r)] for _ in range(len(mat)-r)]
    q=0
    for i in range(len(mat)):
        if i in recurrence_classes:
            q+=1
            continue
        s=0
        for j in range(len(mat[0])):
            if j in recurrence_classes:
                S[i-q][recurrence_classes.index(j)] = mat[i][j]
                s+=1
            else:
                Q[i-q][j-s] = mat[i][j]
    return np.matrix(S), np.matrix(Q)
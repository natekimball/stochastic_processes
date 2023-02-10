import numpy as np
from scipy.linalg import eig 
from fractions import Fraction as frac

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

def main(mat):
    if len(mat) != len(mat[0]):
        print("not a square matrix")
        exit()
    recurrent_classes = scc(mat)
    transient_states = transient(indices, recurrent_classes)
    S,Q = get_S_and_Q(mat, recurrent_classes)
    M = np.linalg.inv(np.identity(len(Q))-Q)
    hitting_probabilities = M*S
    print("recurrent classes:", [[indices[i] for i in c] for c in recurrent_classes])
    print("transient states:", transient_states)
    print("S:\n",S)
    print("Q:\n",Q)
    print("visits:\n",M)
    print("hitting probabilities:\n",hitting_probabilities)
    # print([[frac(str(x)) for x in y] for y in hitting_probabilities])
    print("Nate's probability of winning is %f" % hitting_probabilities[-1,1])
    print("Nate's probability of losing is %f" % hitting_probabilities[-1,0])
    print("Nate's expected winnings is %f" % round(hitting_probabilities[-1,1]*2 - hitting_probabilities[-1,0]*20))
    print("Justin's probability of winning is %f" % hitting_probabilities[0,1])
    print("Justin's probability of losing is %f" % hitting_probabilities[0,0])
    print("Justin's expected winnings is %f" % round(hitting_probabilities[0,1]*20 - hitting_probabilities[0,0]*2))

def dfs(M, i, visited, order):
    visited[i] = True
    for j in range(len(M)):
        if M[i][j] != 0 and not visited[j]:
            dfs(M, j, visited, order)
    order.insert(0,i)

def scc(M):
    visited = [False for _ in range(len(M))]
    order = []
    for i in range(len(M)):
        if not visited[i]:
            dfs(M, i, visited, order)
    classes = []
    visited = [False for _ in range(len(M))]
    while order:
        i = order.pop()
        if not visited[i]:
            cl = []
            dfs(M, i, visited, cl)
            classes.append(cl)
    # print("classes:", classes)
    return get_recurrent(M,classes)

def get_recurrent(M, classes):
    r = len(classes)
    new_mat = [[0 for _ in range(r)] for _ in range(r)]
    for i in range(r):
        for j in range(r):
            for a in classes[i]:
                for b in classes[j]:
                    new_mat[i][j] += M[a][b]
    visited = [False for _ in range(r)]
    l = []
    for i in range(r):
        if not visited[i]:
            only_recurrent(new_mat, i, visited, l)
    new_classes = [classes[i] for i in l]
    return new_classes
    
def only_recurrent(M, i, visited, order):
    visited[i] = True
    has_neighbors = False
    for j in range(len(M)):
        if i!=j and M[i][j] != 0:
            has_neighbors = True
            if not visited[j]:
                dfs(M, j, visited, order)
    if not has_neighbors:
        # order.insert(0,i)
        order.append(i)
    
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

def get_S_and_Q(mat, recurrent):
    rs = []
    for c in recurrent:
        for a in c:
            rs.append(a)
    S = [[0 for _ in range(len(recurrent))] for _ in range(len(mat)-len(rs))]
    Q = [[0 for _ in range(len(mat[0])-len(rs))] for _ in range(len(mat)-len(rs))]
    transient = []
    for i in range(len(mat)):
        if i not in rs:
            transient.append(i)
    
    for i,t in enumerate(transient):
        for j,r in enumerate(recurrent):
            for k in r:
                S[i][j] += mat[t][k]
        for j,t2 in enumerate(transient):
            Q[i][j] = mat[t][t2]

    return np.matrix(S), np.matrix(Q)

if __name__ == "__main__":
    main(mat)

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
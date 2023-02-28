import numpy as np
import util

indices = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
transition_mat = [
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

def solve_reducible(P, indices=None, recurrent_classes=None):
    P = np.array(P)
    if P.shape[0] != P.shape[1]:
        print("not a square matrix")
        exit()
    if indices is None:
        indices = list(range(P.shape[0]))
    if not recurrent_classes:
        recurrent_classes = get_recurrent(P)
    if indices is None:
        indices = list(range(P.shape[0]))
    if not recurrent_classes:
        recurrent_classes = get_recurrent(P)
    transient_states = transient(indices, recurrent_classes)
    S,Q = get_S_and_Q(P, recurrent_classes)
    S,Q = get_S_and_Q(P, recurrent_classes)
    M = np.linalg.inv(np.identity(len(Q))-Q)
    hitting_probabilities = M@S
    hitting_times = M@np.ones((M.shape[0],1))
    hitting_times = M@np.ones((M.shape[0],1))
    print("recurrent classes:", [[indices[i] for i in c] for c in recurrent_classes])
    print("transient states:", transient_states)
    print("S:\n" + util.format_matrix(S))
    print("Q:\n" + util.format_matrix(Q))
    print("visits:\n" + util.format_matrix(M))
    print("hitting times:\n" + util.format_matrix(hitting_times))
    print("hitting probabilities:\n" + util.format_matrix(hitting_probabilities))
    assert np.allclose(np.sum(hitting_probabilities, axis=1), 1)

def get_recurrent(P):
    classes = util.scc(P)
    if len(classes) == 1:
        print("Markov Chain is irreducible")
        util.solve(P)
        exit()
    r = len(classes)
    new_mat = np.zeros((r,r))
    for i in range(r):
        for j in range(r):
            for a in classes[i]:
                for b in classes[j]:
                    new_mat[i,j] += P[a,b]
                    new_mat[i,j] += P[a,b]
    visited = [False for _ in range(r)]
    l = []
    for i in range(r):
        if not visited[i]:
            only_recurrent(new_mat, i, visited, l)
    new_classes = [classes[i] for i in l]
    return new_classes
    
def only_recurrent(P, i, visited, order):
    visited[i] = True
    has_neighbors = False
    for j in range(len(P)):
        if i!=j and P[i,j] != 0:
            has_neighbors = True
            if not visited[j]:
                util.dfs(P, j, visited, order)
                util.dfs(P, j, visited, order)
    if not has_neighbors:
        order.append(i)
    
def transient(indices, recurrent_classes):
    return [r for i,r in enumerate(indices) if find_class(i, recurrent_classes) == -1]

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

    S = np.zeros((mat.shape[0]-len(rs), len(recurrent)))
    Q = np.zeros((mat.shape[0]-len(rs), mat.shape[0]-len(rs)))

    
    transient = [i for i in range(mat.shape[0]) if i not in rs]
    for i,t in enumerate(transient):
        for j,r in enumerate(recurrent):
            for k in r:
                S[i,j]+=mat[t,k]
        for j,t2 in enumerate(transient):
            Q[i,j] = mat[t,t2]

    return S,Q

if __name__ == "__main__":
    solve_reducible(transition_mat, indices)

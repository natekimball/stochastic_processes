import numpy as np

# # transition matrix
# T = np.array([
#     [0.5, 0.5],
#     [0.5, 0.5],
# ])

# # emmision matrix
# M = np.array([
#     [0.4, 0.1, 0.5],
#     [0.1, 0.5, 0.4],
# ])

# # observations
# Y = np.array([3, 1, 1, 3, 2, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 1, 1, 2])

# # initial state
# pi = np.array([0.5, 0.5])

# forward algorithm
def forward(T, M, Y, pi):
    N = len(T)
    T = T.T
    M = M.T
    alpha = np.zeros((N, len(Y)))
    alpha[:,0] = pi * M[Y[0]]
    for t in range(1, len(Y)):
        for i in range(N):
            alpha[i,t] = M[Y[t],i] * np.sum(alpha[:,t-1] * T[i])
    return alpha

# filtering algorithm
def filtering(T, M, Y, pi):
    alpha = forward(T, M, Y, pi)
    return (alpha / np.sum(alpha, axis=0)).T

# backward algorithm
def backward(T, M, Y, pi):
    N = len(T)
    beta = np.zeros((N, len(Y)))
    beta[:,-1] = 1
    for t in range(len(Y)-2, -1, -1):
        for i in range(N):
            beta[i,t] = np.sum(M[:,Y[t+1]] * beta[:,t+1] * T[i])
    
    joint_prob  = np.sum(pi * M[:,Y[0]] * beta[:,0])
    return beta, joint_prob

# smoothing algorithm
def smoothing(T, M, Y, pi):
    alpha = forward(T, M, Y, pi)
    beta, _ = backward(T, M, Y, pi)
    # print("alpha", alpha.T)
    # print("beta", beta.T)
    ab = alpha * beta
    # print("alpha * beta", ab.T)
    return (ab / np.sum(ab, axis=0)).T

# viterbi decoding algorithm
def viterbi(T, M, Y, pi):
    N = len(T)
    T = T.T
    M = M.T
    psi = np.zeros((N, len(Y)))
    parents = np.zeros((N, len(Y)))
    psi[:,0] = pi * M[Y[0]]
    for t in range(1, len(Y)):
        for i in range(N):
            psi[i,t] = M[Y[t],i] * np.max(psi[:,t-1] * T[i])
            parents[i,t] = np.argmax(psi[:,t-1] * T[i])
    # print("psi: \n", psi)
    path = np.zeros(len(Y))
    path[-1] = np.argmax(psi[:,-1])
    for t in range(len(Y)-2, -1, -1):
        path[t] = parents[int(path[t+1]),t+1]
    return path

T = np.array([
    [0, .5, .5],
    [0, 0.9, 0.1],
    [0, 0, 1]
])
M = np.array([
    [0.5, 0.5],
    [0.9, 0.1],
    [0.1, 0.9]
])
pi = np.array([1, 0, 0])
Y = np.array([2, 3, 3, 2, 2, 2, 3, 2, 3]) - 2 
filter = filtering(T, M, Y, pi)
print("filtering: \n", filter)
smooth = smoothing(T, M, Y, pi)
print("smoothing: \n", smooth)
path = viterbi(T, M, Y, pi)
print("decoded path: \n", path)
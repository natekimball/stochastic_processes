import numpy as np

# transition matrix
T = np.array([
    [0.5, 0.5],
    [0.5, 0.5],
])

# emmision matrix
M = np.array([
    [0.4, 0.1, 0.5],
    [0.1, 0.5, 0.4],
])

# initial state
pi = np.array([0.5, 0.5])

# observations
Y = np.array([3, 1, 1, 3, 2, 3, 2, 2, 2, 3, 2, 2, 2, 2, 2, 3, 3, 1, 1, 2]) -1


def main():
    alpha = forward(T, M, Y, pi)
    print("alpha: \n", alpha.T)
    beta, joint_prob = backward(T, M, Y, pi)
    print("beta: \n", beta.T)
    print("joint observation probability: ", joint_prob)
    filter = filtering(T, M, Y, pi)
    print("filtering: \n", filter.T)
    smooth = smoothing(T, M, Y, pi)
    print("smoothing: \n", smooth.T)
    path = np.argmax(smooth, axis=0)
    print("point-wise most likely path: \n", path)
    path = viterbi(T, M, Y, pi)
    print("decoded path: \n", path)
    new_T, new_M, new_pi = baum_welch(T, M, Y, pi)
    print("new transition matrix: \n", new_T)
    print("new emission matrix: \n", new_M)
    print("new initial state: \n", new_pi)
    _, new_joint_prob = backward(new_T, new_M, Y, new_pi)
    print("new joint observation probability: ", new_joint_prob)

# forward algorithm
def forward(T, M, Y, pi):
    N = len(T)
    alpha = np.zeros((N, len(Y)))
    alpha[:,0] = pi * M[:,Y[0]]
    for t in range(1, len(Y)):
        for i in range(N):
            alpha[i,t] = M[:,Y[t]][i] * np.sum(alpha[:,t-1] * T[:,i])
    return alpha

# filtering algorithm
def filtering(T, M, Y, pi):
    alpha = forward(T, M, Y, pi)
    return alpha / np.sum(alpha, axis=0)

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
    return ab / np.sum(ab, axis=0)

# viterbi decoding algorithm
def viterbi(T, M, Y, pi):
    N = len(T)
    T = T.T
    M = M.T
    delta = np.zeros((N, len(Y)))
    parents = np.zeros((N, len(Y)))
    delta[:,0] = pi * M[Y[0]]
    for t in range(1, len(Y)):
        for i in range(N):
            delta[i,t] = M[Y[t],i] * np.max(delta[:,t-1] * T[i])
            parents[i,t] = np.argmax(delta[:,t-1] * T[i])
    # print("delta: \n", delta)
    path = np.zeros(len(Y))
    path[-1] = np.argmax(delta[:,-1])
    for t in range(len(Y)-2, -1, -1):
        path[t] = parents[int(path[t+1]),t+1]
    return path

# hmm learning
def baum_welch(T, M, Y, pi):
    # lambda* = argmax_lambda P(Y1,...Y2;lambda)
    N = len(T)
    alpha = forward(T, M, Y, pi)
    beta, _ = backward(T, M, Y, pi)
    gamma = smoothing(T, M, Y, pi)
    xi = np.zeros((N, N, len(Y)-1))
    for t in range(len(Y)-1):
        for i in range(N):
            for j in range(N):
                xi[i,j,t] = alpha[i,t] * T[i,j] * M[j,Y[t+1]] * beta[j,t+1]
        xi[:,:,t] = xi[:,:,t] / np.sum(xi[:,:,t])
    # print("xi: \n", xi)
    E_transitions = np.sum(xi, axis=2)
    E_visits = np.sum(gamma[:,:-1], axis=1)
    new_T = E_transitions / E_visits[:, np.newaxis]
    new_M = np.zeros_like(M)
    for k in range(M.shape[1]):
        new_M[:,k] = np.sum(gamma[:,Y==k], axis=1) / np.sum(gamma, axis=1)
    new_pi = gamma[:,0]
    return new_T, new_M, new_pi

if __name__ == "__main__":
    main()
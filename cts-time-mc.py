import numpy as np
import sympy as sp
import util


def diagonalize(A):
    evals, Q = np.linalg.eig(A)
    D = np.diag(evals)
    Q_inv = np.linalg.inv(Q)
    assert np.allclose(A,Q@D@Q_inv)
    print("Q:\n", Q)
    # print("Q\n" + util.format_matrix(Q))
    print("D:\n" + util.format_matrix(D))
    print("Q_inv:\n", Q_inv)
    # print("Q_inv\n" + util.format_matrix(Q_inv))
    return Q, D, Q_inv

def compute_Pt(A, t):
    Q, D, Q_inv = diagonalize(A)
    exptA = np.expm(t*A)
    exptD = np.diag(np.exp(t*D.diagonal()))
    eat = Q@exptD@Q_inv
    assert np.allclose(exptA, eat)
    return Q@exptA@Q_inv

def compute_Pt_xy(A, t, x, y):
    Pt = compute_Pt(A, t)
    return Pt[x,y]

def infinitessimal_generator(A):
    np.fill_diagonal(A, -np.sum(A, axis=1))
    print("infinitessimal_generator:\n" + util.format_matrix(A))
    return A

def stat_dist(A):
    shape = A.shape
    new_A = np.append(A,np.zeros(A.shape[0])).reshape(A.shape[0]+1,A.shape[1]).T
    new_A = np.append(new_A,np.ones(A.shape[1]+1)).reshape(A.shape[0]+1,A.shape[1]+1)
    print("solving for stationary distribution:")
    util.print_lin_system(new_A)
    rref = np.array(sp.Matrix(new_A).rref()[0]).astype('float64')
    pi = rref[:-1,-1].flatten()
    print("π: %s" % util.format_array(pi))
    assert np.allclose(pi@A, 0)
    return pi

def A_z(A, recurrent_state):
    Az = np.array([[A[i,j] for j in range(A.shape[1]) if j != recurrent_state] for i in range(A.shape[0]) if i != recurrent_state])
    print("A~z\n" + util.format_matrix(Az))
    return Az

def occupation_times(A, recurrent_state):
    # M = (-Az)^-1
    Az = A_z(A, recurrent_state)
    M = np.linalg.inv(-Az)
    print("occupation_times:\n"+util.format_matrix(M))
    return M

def hitting_times(A, recurrent_state):
    M = occupation_times(A, recurrent_state)
    M1 = M@np.ones((M.shape[0],1)).flatten()
    print("hitting_times:\n"+util.format_array(M1))
    return M1

def expected_time_at(A, state):
    print("E[T] = " + util.format(-1/A[state,state]))

# phi_t(x) = P(X_t = x)
# P_t = P(X_t=y|X_0=x)
# P_t' = P_t@A
# P_t = e^tA
# A = Q@D@Q_inv
# D = Q_inv@A@Q
# e^tA = Q@e^tD@Q_inv = Q@diag(e^t*lambda)@Q_inv

alphas = np.array([
    [0, 1, 1, 0],
    [0, 0, 1, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 0]
])
A = infinitessimal_generator(alphas)
stat_dist(A)
expected_time_at(A, 0)
h = hitting_times(A, 3)
print("time until hitting state 4 from state 1: %d" % h[0])

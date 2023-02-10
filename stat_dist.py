import numpy as np
from scipy.linalg import eig
from fractions import Fraction as frac

transition_mat = np.matrix([
    [.5, .5],
    [.3, .7]
])

S, U = eig(transition_mat.T)
stationary = np.array(U[:,np.isclose(S,1)].flat)
stationary = stationary / np.sum(stationary)
stationary = [str(frac(x).limit_denominator()) for x in stationary]
print(stationary)
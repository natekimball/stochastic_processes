from util import solve
import numpy as np

p = [
    [1/2, 1/4, 1/4],
    [1/4, 1/4, 1/2],
    [0, 1/2, 1/2]
]

indices = [(0,2),(0,1),(1,2),(1,0),(2,1),(2,0),(0,0),(1,1),(2,2)]

new_p = np.zeros((len(p)**2,len(p)**2))

for i in range(len(p)):
    for j in range(len(p)):
        index = indices.index((i,j))
        for k in range(len(p)):
            for l in range(len(p)):
                to = indices.index((k,l))
                new_p[index][to] = p[i][k]*p[j][l]

print(new_p)
solve(new_p, indices, [[6],[7],[8]])
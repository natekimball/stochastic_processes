from util import *
import numpy as np

p = [
    [0, 1/2, 1/2, 0],
    [1/2, 0, 1/2, 0],
    [1/3, 1/3, 0, 1/3],
    [0, 0, 1, 0]
]
print(format_matrix(p))

solve(p)

# recurrence_classes = [[0],[3]]
# solve(p, recurrent_classes=recurrence_classes)
# indices = [1,2,3,4]
# solve(p, indices=indices, recurrent_classes=recurrence_classes)
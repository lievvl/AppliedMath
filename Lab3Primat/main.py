import numpy as np
import matplotlib.pyplot as plt

from SimulateChain import SimChain, AnaliticChain

table = np.array([
    [0.05, 0.5, 0.45, 0., 0., 0., 0., 0.],
    [0.8, 0.1, 0., 0.1, 0., 0., 0., 0.],
    [0., 0.9, 0.1, 0., 0., 0., 0., 0.],
    [0.2, 0., 0., 0.3, 0.45, 0.05, 0., 0.],
    [0., 0.6, 0., 0., 0.2, 0., 0., 0.2],
    [0., 0., 0., 0.2, 0., 0.1, 0.7, 0.],
    [0., 0., 0., 0., 0., 0.4, 0.3, 0.3],
    [0., 0., 0., 0., 0.3, 0.3, 0., 0.4]
])

#table = [
#    [0.2, 0.6, 0.2],
#    [0.4, 0.6, 0],
#    [0, 0.5, 0.5],
#]

initVec = np.array([1, 0, 0, 0, 0, 0, 0, 0])
#initVec = np.array([1, 0, 0])
steps = 30
sC = SimChain(table, initVec, steps)
print("Начальный вектор -", end=' ')
print(initVec)
for i in sC.Simulate():
    print(round(i, 6), end=' ')
print()
sC.PrintErrorsGraph()



initVec = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3])
#initVec = np.array([0, 1, 0])
sC = SimChain(table, initVec, steps)
print("Начальный вектор -", end=' ')
print(initVec)
for i in sC.Simulate():
    print(round(i, 6), end=' ')
sC.PrintErrorsGraph()



print()
print("Аналитическое решение: ")
aC = AnaliticChain(table)
for i in aC.Solve():
    print(round(i, 6), end=' ')
print()
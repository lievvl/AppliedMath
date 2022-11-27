import sys

import numpy as np
import matplotlib.pyplot as plt

class SimChain:
    def __init__(self, table, initVec, steps = None, eps = None):
        self.table = table
        self.vec = initVec
        self.steps = steps
        self.err = np.array([])
        self.eps = eps

    def Simulate(self):
        if (self.eps != None):
            while(True):
                if (len(self.err) != 0) \
                        and (self.err[len(self.err) - 1] < self.eps):
                    break
                self.MakeStep()
        else:
            for i in range(self.steps):
                self.MakeStep()
        return self.vec

    def MakeStep(self):
        newVec = self.vec @ self.table
        self.err = np.append(self.err, self.GetMod(self.vec - newVec))
        self.vec = newVec


    def GetMod(self, vec):
        sum = 0
        for i in vec:
            sum += i * i
        return sum

    def GetErrors(self):
        return self.err

    def PrintErrorsGraph(self):
        x = np.arange(len(self.err))
        plt.plot(x, self.err)
        plt.show()

class AnaliticChain:
    def __init__(self, table):
        self.table = np.zeros((len(table) + 1, len(table) + 1))
        self.err = 1e-8
        for i in range(len(self.table)):
            self.table[0][i] = 1
        for j in range(1, len(self.table)):
            for i in range(0, len(self.table) - 1):
                if (i == j - 1):
                    self.table[i + 1][j - 1] = table[j - 1][i] - 1
                else:
                    self.table[i + 1][j - 1] = table[j - 1][i]

    def Solve(self):
        self.Forward()
        return self.Backwards()

    def Forward(self):
        for i in range(len(self.table) - 1):
            notNullRow = self.SearchFirstNotNullRow(i, i)
            if (notNullRow == -1):
                continue
            self.table[[notNullRow, i]] = self.table[[i, notNullRow]]
            self.table[i] = self.table[i] / self.table[i][i]
            for nulledRow in range(i + 1, len(self.table)):
                mult = -self.table[nulledRow][i] / self.table[i][i]
                self.table[nulledRow] = self.table[nulledRow] + mult * self.table[i]
        if (not self.IsLastRowNull()):
            print('Spanking  A S S')
            sys.exit()
        return self.table

    def SearchFirstNotNullRow(self, column, startRow):
        result = -1
        for row in range(startRow, len(self.table)):
            if (self.table[row][column] != 0):
                result = row
                break
        return result

    def IsLastRowNull(self):
        isNull = True
        lastRow = len(self.table) - 1
        for i in range(len(self.table)):
            if (abs(self.table[lastRow][i]) > self.err):
                isNull = False
                break
        return isNull

    def Backwards(self):
        result = np.zeros(len(self.table) - 1)
        for i in range(len(self.table) - 2, -1, -1):
            sum = 0
            for counted in range(i + 1, len(self.table)):
                if (counted == len(self.table) - 1):
                    result[i] = self.table[i][counted] - sum
                else:
                    sum += self.table[i][counted] * result[counted]
        return result

    def GetTable(self):
        return self.table

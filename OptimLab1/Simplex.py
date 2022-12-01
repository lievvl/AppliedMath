import sys

import numpy as np

def PrintTable(table):
    for row in table:
        print(row)

class Simplex:
    def __init__(self, table, n, m, basis = None):
        self.table = table              # сиплекс таблица
        self.n = n                      # количество переменных
        self.m = m                      # количество ограничений
        self.basis = basis              # базис
        self.err = 1e-8                 # для ошибки округления

    def Calculate(self):
        while not self.IsEnd():
            main_col = self.GetMainColumn()
            main_row = self.GetMainRow(main_col)

            if main_row == -1:
                print(
                    "Не удалось выбрать опорный элемент. "
                    "Задача не имеет решений, так как ОДР не ограничена"
                )
                sys.exit()

            self.basis[main_row] = main_col
            self.NextIteration(main_row, main_col)

        result = np.zeros(self.n)
        for i in range(self.m - 1):
            result[self.basis[i]] = self.table[i][0]
        result[0] = self.table[self.m - 1][0]
        return self.table, result, self.basis

    def IsEnd(self):
        end = True
        for j in range(1, self.n):
            if self.table[self.m - 1][j] < - self.err:
                end = False
                break
        return end

    def GetMainColumn(self):
        column = 1
        for j in range(1, self.n):  #(2,..)
            if self.table[self.m - 1][j] < self.table[self.m - 1][column]:
                column = j
        return column

    def GetMainRow(self, mainCol):
        mainRow = None
        for i in range(self.n - 1): # получить первую допустимую строку
            if self.table[i][mainCol] > self.err:
                mainRow = i
                break

        if mainRow == None:
            return None

        for i in range(mainRow + 1, self.m - 1):    # получить наименьшее отношение
            if (self.table[i][mainCol] > self.err) and (
                    self.table[i][0] / self.table[i][mainCol] <
                    self.table[mainRow][0] / self.table[mainRow][mainCol]):
                mainRow = i

        return mainRow

    def NextIteration(self, main_row, main_col):
        new_table = [np.zeros(self.n) for i in range(self.m)]
        pivotCell = self.table[main_row][main_col]

        for i in range(self.m):
            mult = self.table[i][main_col] / pivotCell
            if i == main_row:
                new_table[i] = self.table[i] / pivotCell
            else:
                new_table[i] = np.subtract(self.table[i], mult * self.table[main_row])

        self.table = new_table

    def SynthBasis(self):
        basis = list()
        tableSynth = [np.zeros(self.m + self.n - 1) for i in range(self.m)]
        optimFunc = np.array(self.table[self.m - 1])

        for i in range(len(tableSynth)):
            for j in range(len(tableSynth[0])):
                if j < self.n:
                    tableSynth[i][j] = self.table[i][j]
                else:
                    tableSynth[i][j] = 0

            if i != self.m - 1:
                tableSynth[i][self.n + i] = 1
                basis.append(self.n + i)



        for j in range(len(tableSynth[0])):
            sum = 0
            for i in range(self.m - 1):
                sum += tableSynth[i][j]
            tableSynth[self.m - 1][j] = -sum
        for basisVar in basis:
            tableSynth[self.m - 1][basisVar] = 0

        subProblem = Simplex(tableSynth, len(tableSynth[0]), len(tableSynth), basis)
        subResultTable, subResult, self.basis = subProblem.solve()

        for j in range(self.n):
            if subResultTable[self.m - 1][j] > self.err:
                print("В методе исскуственного базиса не все искусственные переменные = 0")
                sys.exit()

        new_table = [np.zeros(self.n) for i in range(self.m)]
        for i in range(self.m):
            for j in range(self.n):
                new_table[i][j] = subResultTable[i][j]
        for j in range(self.n):
            sum_col = 0
            for i in range(self.m - 1):
                sum_col += new_table[i][j] * optimFunc[self.basis[i]]
            new_table[self.m - 1][j] = sum_col - optimFunc[j]
        new_table[self.m - 1] = np.array(new_table[self.m - 1]) * (-1)

        self.table = new_table

        return tableSynth, basis

    def solve(self):
        self.optimFunc = np.array(self.table[self.m - 1])
        if (self.basis == None):
            self.SynthBasis()
        return self.Calculate()
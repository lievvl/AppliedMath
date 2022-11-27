import numpy as np
import re

#
# 5.123x_1 -5.23x_2 +453x_3 = 6
#
from Simplex import Simplex


def printTable(table):
    for row in table:
        print(row)

def parseStatement(statement, true_n, full_n):
    mult = 1
    parsed = re.findall(r"[-\+]?\d*\.?\d+x_\d+", statement)
    b = None
    usl = re.findall(r"(>=|=|<=)", statement)[0];
    if (re.findall(r"= [-\+]?\d*\.?\d", statement) != []):
        b = re.findall(r"= [-\+]?\d*\.?\d", statement)[0];
        b = float(b[2:])
        result = [];
        if (b < 0):
            mult = -1
            b = abs(b)
            if (usl == ">="):
                usl = "<="
            elif (usl == "<="):
                usl = ">="

    if (usl == "="):
        result = np.zeros(full_n)
    if (usl == ">="):
        result = np.zeros(full_n + 1)
        result[-1] = -1
    if (usl == "<="):
        result = np.zeros(full_n + 1)
        result[-1] = 1

    for i in range(1, true_n + 1):
        searchedX = "x_" + str(i)
        for x in parsed:
            if (re.compile(searchedX).findall(x) != []):
                found = re.findall(r'[-\+]?\d*\.?\d+x', x)[0]
                found = float(found[:len(found) - 1])
                parsed.remove(x)
                result[i - 1] = mult * found
                break
    result = np.r_[b, result]
    return result

true_n = 0
full_n = 0
m = 0
A = []
b = []

print(np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])[:1])
true_n = int(input('Введите количество переменных = '))
full_n = true_n
m = int(input('Введите количество ограничений = '))
print('Ввод уравнений в формате: \"5.123x_1 -5.23x_2 +453x_3 >= -6\"')
for i in range(0, m):
    inp = input()
    parseResult = parseStatement(inp, true_n, full_n)
    if (len(parseResult) > full_n + 1):
        for i in range(0, len(A)):
            A[i] = np.append(A[i], 0.0)
        full_n += 1
    A.append(parseResult)
min_max = input('f -> min/max?\n')
func = input('Ввод целевой функции в формате: \"5.123x_1 -5.23x_2 +453x_3\"\n')
func = func + " = 0"
func = parseStatement(func, true_n, full_n)
if (min_max == "max"):
    func = func * (-1)

basis = None
if input('Начальная точка? (y/n): ') == "y":
    print('Ввод начальной точки в формате \"1 2 3 4 5\"')
    startPoint = input()
    startPoint = startPoint.split(' ')
    basis = []
    for i in range(len(startPoint)):
        x = float(startPoint[i])
        if x != 0:
            basis.append(i + 1)

print(basis)
A.append(func)
printTable(A)
s = Simplex(A, full_n + 1, m + 1)
table, result, _ = s.solve()


for i in result:
    print(round(i, 5), end=' ')
print()

print(-result[0])
print(result @ func.transpose())

# task 1
# 4
# 2
# 3x_1 +1x_2 -1x_3 +1x_4 = 4
# 5x_1 +1x_2 +1x_3 -1x_4 = 4
# min
# -6x_1 -1x_2 -4x_3 +5x_4
# y
# 1 0 0 1

# task 5
# 4
# 2
# 1x_1 +1x_2 -1x_3 -10x_4 = 0
# 1x_1 +14x_2 +10x_3 -10x_4 = 11
# min
# -1x_1 +4x_2 -3x_3 +10x_4
# n

# task 6
# 4
# 2
# 1x_1 +3x_2 +3x_3 +1x_4 <= 3
# 2x_1 +3x_3 -1x_4 <= 4
# min
# -1x_1 +5x_2 +1x_3 -1x_4
# n

# task 7
# 5
# 3
# 3x_1 +1x_2 +1x_3 +1x_4 -2x_5 = 10
# 6x_1 +1x_2 +2x_3 +3x_4 -4x_5 = 20
# 10x_1 +1x_2 +3x_3 +6x_4 -7x_5 = 30
# min
# -1x_1 -1x_2 +1x_3 -1x_4 +2x_5
# n




